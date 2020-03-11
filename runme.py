import can
import mppts


can_interface ='slcan0'
bus = can.interface.Bus(can_interface, bustype='socketcan')
mppt_full = can.Message(arbitration_id=0x711, data=[255, 255, 255, 255, 255, 255, 255, 255])
mppt_send = can.Message(arbitration_id=0x712)
can.send_periodic('slcan0', mppt_send, 0.10)
test = mppts.Drivetek(1810)
#while True:
#   msg = bus.recv()
#   test.parse_can_msg(msg.arbitration_id, msg.data)
