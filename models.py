from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Date, Enum
)
from sqlalchemy.orm import relationship
from database import Base
import enum

class VidImot(enum.Enum):
    sobstven = "собствен"
    naet = "нает"
    sasobsven = "съсобствен"


class NTP(enum.Enum):
    niva = "нива"
    ovoshki = "овощна градина"
    loze = "лозе"
    pasishte = "пасище"
    gora = "гора"
    poliana = "поляна"
    drugo = "друго"

class Imot(Base):
    __tablename__ = "imoti"

    id = Column(Integer, primary_key=True)

    ecatte = Column(String, nullable=False)
    imot_nomer = Column(String, nullable=False)

    obshta_plosht = Column(Float, nullable=False)

    plosht_sobstvena = Column(Float, nullable=True)
    plosht_naeta = Column(Float, nullable=True)

    vid = Column(Enum(VidImot), nullable=False)
    ntp = Column(Enum(NTP), nullable=False)

    mestnost = Column(String, nullable=True)
    kategoriya = Column(String, nullable=True)

    zabelezhka = Column(String, nullable=True)

    # relationships
    dokumenti = relationship("Dokument", back_populates="imot", cascade="all, delete")
    naemi = relationship("Naem", back_populates="imot", cascade="all, delete")
    

class Dokument(Base):
    __tablename__ = "dokumenti"

    id = Column(Integer, primary_key=True)
    imot_id = Column(Integer, ForeignKey("imoti.id"))

    ime = Column(String, nullable=False)
    tip = Column(String, nullable=False)  # договор, нотариален акт и др.
    filepath = Column(String, nullable=False)

    imot = relationship("Imot", back_populates="dokumenti")


class Naem(Base):
    __tablename__ = "naemi"

    id = Column(Integer, primary_key=True)

    imot_id = Column(Integer, ForeignKey("imoti.id"), nullable=False)
    dogovor_id = Column(Integer, ForeignKey("dogovori.id"), nullable=False)  # ✅ НОВО

    plosht_dka = Column(Float, nullable=False)
    cena_na_dka = Column(Float, nullable=False)

    data_nachalo = Column(Date, nullable=False)
    data_krai = Column(Date, nullable=True)

    tip = Column(String, nullable=False)
    zabelezhka = Column(String, nullable=True)

    imot = relationship("Imot", back_populates="naemi")
    dogovor = relationship("Dogovor", back_populates="naemi")


class Dogovor(Base):
    __tablename__ = "dogovori"

    id = Column(Integer, primary_key=True)

    nomer = Column(String, nullable=False)
    data = Column(Date, nullable=False)

    tip = Column(String, nullable=False)
    # "наем", "аренда", "съсобственост", "собственост"

    filepath = Column(String, nullable=False)
    zabelezhka = Column(String, nullable=True)

    naemi = relationship("Naem", back_populates="dogovor", cascade="all, delete")