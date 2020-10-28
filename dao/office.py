from global_var import Base
from sqlalchemy import *


class Office(Base):
    __tablename__ = 'office'
    id = Column(Integer, primary_key=True, autoincrement=True)
    office_name = Column(String(32), unique=True)
    office_address = Column(String(64), nullable=True)
    office_telephone = Column(String(16), nullable=True)
