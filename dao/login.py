from global_var import Base
from sqlalchemy import *


class Login(Base):
    __tablename__ = "login"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
