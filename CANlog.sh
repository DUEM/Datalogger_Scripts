#!/bin/bash

# enable can0
# sudo ip link set can0 down
# sudo ip link set can0 type can bitrate 1000000
# sudo ip link set can0 up

# Wait until ttyCAN exists
while [ ! -L /dev/ttyCAN ]; do sleep 1; echo notfound; done
echo found
sleep 1

# enable slcan0
# slcand -o -c -f -s4 -S57600 /dev/ttyCAN slcan0 > /home/pi/Datalogger_Scripts/slcand_errors.txt
slcand -o -f -s4 -S57600 /dev/ttyCAN slcan0 > /home/pi/Datalogger_Scripts/slcand_errors.txt
sleep 1
ifconfig slcan0 up > /home/pi/Datalogger_Scripts/ifconfig_errors.txt

# activate venv
		source /home/pi/Datalogger_Scripts/.venv/bin/activate

# run CANlog.py
python3 -u /home/pi/Datalogger_Scripts/CANlog.py slcan0
