from sqlalchemy import *
from global_var import Base


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(String(10), unique=True)
    bed_number = Column(Integer)
    oid = Column(Integer, ForeignKey('office.id'))
