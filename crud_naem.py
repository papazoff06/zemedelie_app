from sqlalchemy.orm import Session
from database import SessionLocal
from models import Naem, Dogovor
from datetime import date

def create_naem(
    imot_id,
    dogovor_id,
    plosht_dka,
    cena_na_dka,
    data_nachalo,
    data_krai=None,
    tip="наем",
    zabelezhka=None
):
    session = SessionLocal()

    naem = Naem(
        imot_id=imot_id,
        dogovor_id=dogovor_id,
        plosht_dka=plosht_dka,
        cena_na_dka=cena_na_dka,
        data_nachalo=data_nachalo,
        data_krai=data_krai,
        tip=tip,
        zabelezhka=zabelezhka
    )

    session.add(naem)
    session.commit()
    session.refresh(naem)
    session.close()

    return naem

def dogovori_za_imot(imot_id):
    session = SessionLocal()

    dogovori = (
        session.query(Dogovor)
        .join(Naem)
        .filter(Naem.imot_id == imot_id)
        .all()
    )

    session.close()
    return dogovori