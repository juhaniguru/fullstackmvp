# coding: utf-8
import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text, create_engine
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

load_dotenv()

engine = create_engine(os.getenv('CONNECTION_STRING'))
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = SessionLocal()
    print("###############open")
    try:
        yield db
    finally:
        print("####################clsoe")
        db.close()


Db = Annotated[Session, Depends(get_db)]


class Environmenttype(Base):
    __tablename__ = 'environmenttype'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, unique=True)


class Inspectiontargettype(Base):
    __tablename__ = 'inspectiontargettype'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, unique=True)


class Inspectiontype(Base):
    __tablename__ = 'inspectiontype'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, unique=True)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, unique=True)
    address = Column(String(45), nullable=False)
    zip_code = Column(String(45), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    role = Column(String(45), nullable=False)
    password = Column(String(255), nullable=False)
    access_token_identifier = Column(String(45))
    refresh_token_identifier = Column(String(45))


class Environment(Base):
    __tablename__ = 'environment'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(Text)
    location_id = Column(ForeignKey('location.id'), nullable=False, index=True)
    environmenttype_id = Column(ForeignKey('environmenttype.id'), nullable=False, index=True)

    environmenttype = relationship('Environmenttype')
    location = relationship('Location')
    users = relationship('User', secondary='userresponsibleenvironment')


class Inspectiontarget(Base):
    __tablename__ = 'inspectiontarget'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(Text)
    createdAt = Column(DateTime, nullable=False)
    environment_id = Column(ForeignKey('environment.id'), nullable=False, index=True)
    inspectiontargettype_id = Column(ForeignKey('inspectiontargettype.id'), nullable=False, index=True)

    environment = relationship('Environment')
    inspectiontargettype = relationship('Inspectiontargettype')
    users = relationship('User', secondary='userresponsibletarget')


t_userresponsibleenvironment = Table(
    'userresponsibleenvironment', metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True, nullable=False, index=True),
    Column('environment_id', ForeignKey('environment.id'), primary_key=True, nullable=False, index=True)
)


class Inspectionform(Base):
    __tablename__ = 'inspectionform'

    id = Column(Integer, primary_key=True)
    createdAt = Column(DateTime, nullable=False)
    closedAt = Column(DateTime)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    environment_id = Column(ForeignKey('environment.id'), index=True)
    inspectiontarget_id = Column(ForeignKey('inspectiontarget.id'), index=True)
    inspectiontype_id = Column(ForeignKey('inspectiontype.id'), nullable=False, index=True)

    environment = relationship('Environment')
    inspectiontarget = relationship('Inspectiontarget')
    inspectiontype = relationship('Inspectiontype')
    user = relationship('User')


class Instruction(Base):
    __tablename__ = 'instruction'

    id = Column(Integer, primary_key=True)
    title = Column(String(45), nullable=False)
    description = Column(Text)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime)
    inspectiontarget_id = Column(ForeignKey('inspectiontarget.id'), nullable=False, index=True)
    created_by = Column(ForeignKey('user.id'), nullable=False, index=True)
    updated_by = Column(ForeignKey('user.id'), index=True)

    user = relationship('User', primaryjoin='Instruction.created_by == User.id')
    inspectiontarget = relationship('Inspectiontarget')
    user1 = relationship('User', primaryjoin='Instruction.updated_by == User.id')


t_userresponsibletarget = Table(
    'userresponsibletarget', metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True, nullable=False, index=True),
    Column('inspectiontarget_id', ForeignKey('inspectiontarget.id'), primary_key=True, nullable=False, index=True)
)


class Inspectionresult(Base):
    __tablename__ = 'inspectionresult'

    id = Column(Integer, primary_key=True)
    createdAt = Column(DateTime, nullable=False)
    value = Column(Integer, nullable=False)
    note = Column(Text)
    title = Column(Text, nullable=False)
    inspectionform_id = Column(ForeignKey('inspectionform.id'), nullable=False, index=True)

    inspectionform = relationship('Inspectionform')
