# Fuck me.
"""
Created by yours truly

MPPTs need to be sent an empty CAN message with arbitration/message ID 0x710 + offset - we have 711 and 712
Offset being 1-15 based on switches on MPPTs
MPPTs will need different offsets configured so that returned messages don'e interfere.
MPPTs will return status information on CAN id: (sent ID +48 or =96 for some reason...)
Current / voltages will need multiplying by client specific value to find our real values

I don't know wtf I'm doing
"""
import struct
import can

from enum import IntFlag
class mpptFlag(IntFlag):
    BVLR = 128
    OVT = 64
    NOC = 32
    UNDV = 16

class Drivetek(object):
    """ Drivetec MPPT Class

    Keyword Arguments:
    mppt_base_addres -- Integer, MPPT base addresses are 1809, and 1810 (0x700)
    Will need to split this up
    """

    def __init__(self, mppt_base_address, name): #1810, 1811
        
        self.statdict = dict(name=name,
                             BVLR=None,
                             OVT=None,
                             NOC=None,
                             UNDV=None,
                             UIN=None,
                             IIN=None,
                             UOUT=None,
                             tamb=None)

        self.return_id = mppt_base_address+96

        self.can_range = [mppt_base_address, self.return_id]
    
    def status(self):
        return self.statdict

    def parse_can_msg(self, can_id, can_data):
        if(can_id == self.return_id): #self.return_id
            unpacked = struct.unpack('BBBBBBB', can_data);
            flags = unpacked[0]
            first_flag = mpptFlag(flags)

            uin_mult = 0.15049
            iin_mult = 0.00872
            uout_mult = 0.20879

            uin_msb = (flags % 4) * 256
            uin_lsb = unpacked[1]
            uin = (uin_msb + uin_lsb)*uin_mult
            
            iin_msb = (unpacked[2] % 4) * 256
            iin_lsb = unpacked[3]
            iin = (iin_msb + iin_lsb)*iin_mult

            uout_msb = (unpacked[4] % 4) * 256
            uout_lsb = unpacked[5]
            uout = (uout_msb + uout_lsb)*uout_mult

            tamb = unpacked[6]

            self.statdict["BVLR"]= mpptFlag.BVLR in first_flag
            self.statdict["OVT"]= mpptFlag.OVT in first_flag
            self.statdict["NOC"]= mpptFlag.NOC in first_flag
            self.statdict["UNDV"]= mpptFlag.UNDV in first_flag
            self.statdict["UIN"]= uin
            self.statdict["IIN"]= iin
            self.statdict["UOUT"]= uout
            self.statdict["tamb"]= tamb
            print(self.statdict)
        else:
            return False
        return True

        try:
            msg_type = self.types[can_id]
        except KeyError:
            return 0
        try:
            msg_format = self.formats[msg_type]
        except KeyError:
            msg_format = "2*float32"

        if msg_format == "u_int32 + char[4]":
            pass
        #elif msg_format == "3*u_int16":
        else:
            first, second = struct.unpack("ff", can_data)
            self._cangroups[msg_type] = (second, first)
        return 1
