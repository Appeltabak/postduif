from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, \
    Text, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref

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

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')


class Flight(Base):
    __tablename__ = 'flight'

    id = Column(Integer, primary_key=True)
    duif_id = Column(Integer, ForeignKey('duif.id'))
    start_time = Column(Integer)
    end_time = Column(Integer)
    msg_id = Column(Integer, ForeignKey('msg.id'))


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    msg = Column(Text)
    receiver_id = Column(Integer, ForeignKey('user.id'))
    sender_id = Column(Integer, ForeignKey('user.id'))
    sealed = Column(Boolean)
    status = Column(Integer)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))
    salt = Column(String(50))
    mail = Column(String(50))
    loc = Column(String(100))

session = Session()
for duif in session.query(Duif):
    print(duif)