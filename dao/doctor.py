from global_var import Base
from sqlalchemy import *


class Doctor(Base):
    __tablename__ = 'doctor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_number = Column(String(20), unique=True)
    name = Column(String(6))
    gender = Column(Integer)
    age = Column(Integer)
    title = Column(String(10))
    oid = Column(Integer, ForeignKey('office.id'))
