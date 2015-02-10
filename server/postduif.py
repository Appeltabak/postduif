from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///database.db', echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Duif(Base):
    __tablename__ = 'duif'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    speed = Column(Integer)
    level = Column(Integer)
    state = Column(Enum)
    home_loc = Column(String)

    user_id = relationship()


class Flight(Base):
    __tablename__ = 'flight'

    id = Column(Integer, primary_key=True)
    duif_id = Column(ForeignKey('duif_id'))
    start_time = Column(Integer)
    end_time = Column(Integer)
    msg_id = Column(ForeignKey('msg_id'))
    