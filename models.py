from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Deklarator(Base):
    __tablename__ = "deklarator"

    id = Column(Integer, primary_key=True)
    ime = Column(String)
    egn = Column(String)
    telefon = Column(String)

    imoti = relationship("Imot", secondary="deklarator_imot")


class Imot(Base):
    __tablename__ = "imot"

    id = Column(Integer, primary_key=True)
    imot_nomer = Column(String, unique=True)
    plosht = Column(Float)
    vid = Column(String)  # sobstven / naet / sasobshtven
    procent = Column(Float)


class DeklaratorImot(Base):
    __tablename__ = "deklarator_imot"

    deklarator_id = Column(Integer, ForeignKey("deklarator.id"), primary_key=True)
    imot_id = Column(Integer, ForeignKey("imot.id"), primary_key=True)
