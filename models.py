from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Date, Enum
)
from sqlalchemy.orm import relationship
from database import Base
import enum


# ─────────────────────────────
# ENUMS
# ─────────────────────────────

class NTP(enum.Enum):
    niva = "нива"
    ovoshki = "овощна градина"
    loze = "лозе"
    pasishte = "пасище"
    gora = "гора"
    poliana = "поляна"
    drugo = "друго"


class TipDokument(enum.Enum):
    naem = "наем"
    arenda = "аренда"
    sobstvenost = "собственост"


class TipPravo(enum.Enum):
    naem = "наем"
    arenda = "аренда"
    sobstvenost = "собственост"


# ─────────────────────────────
# ИМОТ (КАДАСТЪР)
# ─────────────────────────────

class Imot(Base):
    __tablename__ = "imoti"

    id = Column(Integer, primary_key=True)

    ecatte = Column(String, nullable=False)
    imot_nomer = Column(String, nullable=False)

    plosht_kadastr = Column(Float, nullable=False)

    ntp = Column(Enum(NTP), nullable=False)
    kategoriya = Column(String, nullable=True)
    mestnost = Column(String, nullable=True)

    zabelezhka = Column(String, nullable=True)

    prava = relationship(
        "PravoImot",
        back_populates="imot",
        cascade="all, delete"
    )


# ─────────────────────────────
# ДОКУМЕНТ
# ─────────────────────────────

class Dokument(Base):
    __tablename__ = "dokumenti"

    id = Column(Integer, primary_key=True)

    nomer = Column(String, nullable=False)
    data = Column(Date, nullable=False)

    tip = Column(Enum(TipDokument), nullable=False)

    filepath = Column(String, nullable=False)
    zabelezhka = Column(String, nullable=True)

    prava = relationship(
        "PravoImot",
        back_populates="dokument",
        cascade="all, delete"
    )


# ─────────────────────────────
# ПРАВО ВЪРХУ ИМОТ
# ─────────────────────────────

class PravoImot(Base):
    __tablename__ = "prava_imoti"

    id = Column(Integer, primary_key=True)

    imot_id = Column(Integer, ForeignKey("imoti.id"), nullable=False)
    dokument_id = Column(Integer, ForeignKey("dokumenti.id"), nullable=False)

    tip_pravo = Column(Enum(TipPravo), nullable=False)

    plosht_pravo = Column(Float, nullable=False)
    cena_na_dka = Column(Float, nullable=True)

    data_nachalo = Column(Date, nullable=False)
    data_krai = Column(Date, nullable=True)

    zabelezhka = Column(String, nullable=True)

    imot = relationship("Imot", back_populates="prava")
    dokument = relationship("Dokument", back_populates="prava")