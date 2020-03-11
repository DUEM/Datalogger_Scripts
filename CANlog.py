#!/bin/python3
"""
Created on Thu 28 Apr 2016 17:36:32 BST

Logs CAN messages to mysql server

@author: Adam Leach adam.leach@dur.ac.uk, qazwsxalan@gmail.com
"""
import controls
import motors
import batteries
import mppts
import datetime
import json
import os
import sys
import can
from time import sleep
import time
from can.interfaces import socketcan_native as native_bus

import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
import dbstorage



from multiprocessing import Process, Queue


queue = Queue()

def mysql_log(q):
    # mysql config
    username = "root"
    database = "2019"
    # host = "192.168.7.2"
    host = "127.0.0.1"
    password = "dusc2015"
    serveraddr = "mysql+mysqlconnector://%s:%s@%s/%s" % (
        username, password, host, database)
    # mysql setup
    engine = sqla.create_engine(serveraddr, pool_recycle=3600)
    dbstorage.Base.metadata.create_all(engine)
    session_init = sessionmaker(bind=engine)
    session = session_init()
    # Set up bus object ORM interfaces
#%======================================================
    can_orms = [dbstorage.WS20_ORM, dbstorage.Controls_ORM, dbstorage.BMS_ORM, dbstorage.Drivetek_ORM]
#=======================================================
    while True:
        if not queue.empty():
            i, changed = queue.get()
            sys.stdout.flush()
            sys.stderr.flush()
            active_orm = can_orms[i]
            session.add(active_orm(**changed))
            # Commiting every message might strain server,
            # setting transaction flushes to occur
            # once per second should help
            if queue.empty():
                session.commit()
        else:
            sleep(0.1)



# can config
motor_base_id = int("0x600", 16)
driver_base_id = int("0x500", 16)
can_interface = sys.argv[1]
print(can_interface)
bus = native_bus.SocketscanNative_Bus(channel=can_interface)

# Set up bus objects
motor = motors.Wavesculptor20(mc_base_address=motor_base_id)
controls = controls.Controls(controls_base_address=driver_base_id)
bms = batteries.orionBMS()
mppt_woof = mppts.Drivetek(1809, 'woof')    #Different addresses
mppt_javed = mppts.Drivetek(1810, 'javed')
can_objects = [motor, controls, bms, mppt_woof, mppt_javed]

# Set up bus object shared memory files:
motor_file = "/dev/shm/motor"
controls_file = "/dev/shm/controls"
bms_file = "/dev/shm/bms"
mppt_woof_file = "/dev/shm/mppt_woof"
mppt_javed_file = "dev/shm/mppt_javed"
can_files = [motor_file, controls_file, bms_file, mppt_woof_file, mppt_javed_file]

# intial file setup prevents file not found errors

for i, active_obj in enumerate(can_objects):
    data = active_obj.status()
    data["time"] = datetime.datetime.now().isoformat()
    json.dump(data, open(can_files[i], "w"))

COMMIT_RATE = 60
p = Process(target=mysql_log, args=(queue,))
p.start()
woof_send = can.Message(arbitration_id=0x711, extended_id=False)
javed_send = can.Message(arbitration_id=0x712, extended_id=False)
currtime = datetime.datetime.now()
while 1:
    print("waiting for message")
    msg = bus.recv(timeout=1)
    if msg:
        print(msg.arbitration_id, msg.data)
        for i, active_obj in enumerate(can_objects):
            if msg.arbitration_id in active_obj.can_range:
                # Get a copy of old data, update and count changes
                old_data = active_obj.status().copy()
                active_obj.parse_can_msg(msg.arbitration_id, msg.data)
                data = active_obj.status()
                data["time"] = datetime.datetime.now().isoformat()
                changed = {}
                for key in old_data:
                    # only log updated values, saves space.
                    # SQLalchemy needs to be explicitly told a key is NULL
                    if data[key] == old_data[key]:
                        changed[key] = None
                    else:
                        changed[key] = data[key]
                changed["time"] = datetime.datetime.now()
                jsonfile = open(can_files[i], "w")
                json.dump(data, jsonfile)
                # print(data)
                jsonfile.flush()
                os.fsync(jsonfile.fileno())
                jsonfile.close()
                queue.put((i, changed))
    if datetime.datetime.now()-currtime > datetime.timedelta(seconds=1):
        currtime = datetime.datetime.now()
        bus.send(woof_send)
        bus.send(javed_send)
