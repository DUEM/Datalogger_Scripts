# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:31:48 2016

@author:  Adam Leach (adam.leach@durham.ac.uk, qazwsxalan@gmail.com)
"""
import struct


class orionBMS(object):
    """ Orion BMS Class

    Keyword Arguments:
    bms_base_address -- Integer, OrionBMS's base address,
                       default 1536 (0x600)
    """

    def __init__(self, bms_base_address=0x700):
        self.statdict = dict(cellVmin=None,
                             cellVmax=None,
                             cellVavg=None,
                             packCurr=None,
                             tempmax=None,
                             tempmin=None,
                             tempavg=None,
                             SoC=None,
                             curr=None,
                             pVolt=None,
                             pSumVolt=None,
                             DCLim=None,
                             CCLim=None,
                             relayState=None,
                             currState=None)

    def status(self):
        """returns a dict of BMS status"""
        return self.statdict

    def parse_can_msg(self, can_id, can_data):
        """Parses CAN msg, from SQL db or CAN Network, updates internal state

        Returns true if ID matches.
        Arguments:
        can_id   -- Integer, message ID from CAN network, determines frame type
        can_data -- Raw bits from CAN Data field, frame type tells us format
        """

        if can_id == 0x700:
            Vmax, Vmin, Vavg = struct.unpack("HHH", can_data)
            self.statdict['cellVmin'] = 0.0001 * Vmin
            self.statdict['cellVmax'] = 0.0001 * Vmax
            self.statdict['cellVavg'] = 0.0001 * Vavg
        elif can_id == 0x701:
            tH, tL, TA, DCL, CCL, cState = struct.unpack("bbbBBB", can_data)
            self.statdict['tempmax'] = tH
            self.statdict['tempmin'] = tL
            self.statdict['tempavg'] = tA
            self.statdict['DCLim'] = DCL
            self.statdict['CCLim'] = CCL
            self.statdict['currState'] = cState
        elif can_id == 0x702:
            SoC, pCurr, PInstV, PSumV, rState = struct.unpack("BhbBBB", can_data)
            self.statdict['SoC'] = 0.5*SoC
            self.statdict['curr'] = 0.1*pCurr
            self.statdict['pVolt'] = PInstV
            self.statdict['pSumVolt'] = PSumV
            self.statdict['relayState'] = rState
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

        if msg_format == "u_int32 + char[4]":  # Identification information
            pass  # These Values should not change

        elif msg_format == "3*u_int16":  # Status Information
            '''
            # Just rewrite this entire, awful, section. It never worked.
            self.a = [0,0,0,0,0,0,0,0]
            self.b = [0,0,0,0,0,0,0,0]
            #Awful hacky bit flags
            self.a,self.b,self.c,self.d = struct.unpack("hhhh",can_data)
            self.limits["HeatS"]        = bin(self.a)[0]
            self.limits["BusVL"]        = bin(self.a)[1]
            self.limits["BusVU"]        = bin(self.a)[2]
            self.limits["BusC"]         = bin(self.a)[3]
            self.limits["Velo"]         = bin(self.a)[4]
            self.limits["MotorC"]       = bin(self.a)[5]
            self.limits["PWM"]          = bin(self.a)[6]


            self.errors["15VUVL"]  = bin(self.b)[-7]
            self.errors["Conf"]    = bin(self.b)[-6]
            self.errors["Watch"]   = bin(self.b)[-5]
            self.errors["Halls"]   = bin(self.b)[-4]
            self.errors["DCBusOV"] = bin(self.b)[-3]
            self.errors["SoftOC"]  = bin(self.b)[-2]
            self.errors["HardOC"]  = bin(self.b)[-1]

            self.activeMotor = self.c
            '''
        else:
            first, second = struct.unpack("ff", can_data)
            self._cangroups[msg_type] = (second, first)
        return 1
