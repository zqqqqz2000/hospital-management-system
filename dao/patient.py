from sqlalchemy import *
from global_var import Base


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True)
    did = Column(Integer, ForeignKey('doctor.id'))
    rid = Column(Integer, ForeignKey('room.id'))
    oid = Column(Integer, ForeignKey('office.id'))
    history_number = Column(String(20))
    name = Column(String(6))
    gender = Column(Integer)
    age = Column(Integer)
    diagnose = Column(String(512))
