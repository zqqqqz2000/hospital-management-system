from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://root:@localhost:3306/hospital",
    encoding="utf-8",
    echo=True
)
DBSession = sessionmaker(bind=engine)


def init():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
