import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DATETIME
Base = declarative_base()


class WS20_ORM(Base):
    ''' Object-Relational Map for Wavesculptor 20
    '''
    __tablename__ = 'motorstate'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    time = sqla.Column(DATETIME(fsp=4))
    busCurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    busVoltage = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vehicleVelocity = sqla.Column(sqla.Float, server_default=None, nullable=True)
    motorVelocity = sqla.Column(sqla.Float, server_default=None, nullable=True)
    phaseACurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    phaseBCurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vectVoltReal = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vectVoltImag = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vectCurrReal = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vectCurrImag = sqla.Column(sqla.Float, server_default=None, nullable=True)
    backEMFReal = sqla.Column(sqla.Float, server_default=None, nullable=True)
    backEMFImag = sqla.Column(sqla.Float, server_default=None, nullable=True)
    fifteenVsupply = sqla.Column(sqla.Float, server_default=None, nullable=True)
    onesixfiveVsupply = sqla.Column(sqla.Float, server_default=None, nullable=True)
    twofiveVsupply = sqla.Column(sqla.Float, server_default=None, nullable=True)
    onetwoVsupply = sqla.Column(sqla.Float, server_default=None, nullable=True)
    fanSpeed = sqla.Column(sqla.Float, server_default=None, nullable=True)
    fanDrive = sqla.Column(sqla.Float, server_default=None, nullable=True)
    heatSinkTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    motorTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    airInletTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    processorTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    airOutletTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    capacitorTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    DCBusAmpHours = sqla.Column(sqla.Float, server_default=None, nullable=True)
    Odometer = sqla.Column(sqla.Float, server_default=None, nullable=True)

    def __repr__(self):
        return "<WS20_ORM(busCurrent='%s', busVoltage='%s', \
                vehicleVelocity='%s')>" % (
                self.busCurrent, self.busVoltage, self.vehicleVelocity)


class Controls_ORM(Base):
    __tablename__ = 'controls'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    time = sqla.Column(DATETIME(fsp=4))
    setBusCurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    setMotorCurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    setMotorVelocity = sqla.Column(sqla.Float, server_default=None, nullable=True)

class BMS_ORM(Base):
    __tablename__ = 'batteries'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    time = sqla.Column(DATETIME(fsp=4))
    cellVmin = sqla.Column(sqla.Float)
    cellVmax = sqla.Column(sqla.Float)
    cellVavg = sqla.Column(sqla.Float)
    packCurr = sqla.Column(sqla.Float)
    tempmax = sqla.Column(sqla.Float)
    tempmin = sqla.Column(sqla.Float)
    tempavg = sqla.Column(sqla.Float)
    SoC = sqla.Column(sqla.Float)
    pVolt = sqla.Column(sqla.Float)
    pSumVolt = sqla.Column(sqla.Float)
    DCLim = sqla.Column(sqla.Float)
    CCLim = sqla.Column(sqla.Float)
    relayState = sqla.Column(sqla.Integer)
    currState = sqla.Column(sqla.Integer)


class GPS_ORM(Base):
    __tablename__ = 'gps_tpv'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    device = sqla.Column(sqla.String(13))
    tag = sqla.Column(sqla.String(40))
    mode = sqla.Column(sqla.SmallInteger)
    time = sqla.Column(DATETIME(fsp=4))
    ept = sqla.Column(sqla.Float) 
    lat = sqla.Column(sqla.Float) 
    lon = sqla.Column(sqla.Float) 
    alt = sqla.Column(sqla.Float) 
    epx = sqla.Column(sqla.Float) 
    epy = sqla.Column(sqla.Float) 
    epv = sqla.Column(sqla.Float) 
    track = sqla.Column(sqla.Float) 
    speed = sqla.Column(sqla.Float) 
    climb = sqla.Column(sqla.Float) 
    epd = sqla.Column(sqla.Float) 
    eps = sqla.Column(sqla.Float) 
    epc = sqla.Column(sqla.Float)


class Drivetek_ORM(Base):
    __tablename__ = 'mppts'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    time = sqla.Column(DATETIME(fsp=4))
    name = sqla.Column(sqla.String(13))
    BVLR = sqla.Column(sqla.Boolean)
    OVT = sqla.Column(sqla.Boolean) 
    NOC = sqla.Column(sqla.Boolean)
    UNDV = sqla.Column(sqla.Boolean)
    UIN = sqla.Column(sqla.Float) 
    IIN = sqla.Column(sqla.Float) 
    UOUT = sqla.Column(sqla.Float) 
    tamb = sqla.Column(sqla.Float) 
