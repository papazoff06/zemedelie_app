from sqlalchemy.orm import Session
from database import SessionLocal
from models import Dogovor
from datetime import date

def create_dogovor(
    nomer: str,
    data: date,
    tip: str,
    filepath: str,
    zabelezhka: str | None = None
):
    db: Session = SessionLocal()
    try:
        dogovor = Dogovor(
            nomer=nomer,
            data=data,
            tip=tip,
            filepath=filepath,
            zabelezhka=zabelezhka
        )
        db.add(dogovor)
        db.commit()
        db.refresh(dogovor)
        return dogovor
    finally:
        db.close()


def get_dogovor(dogovor_id: int):
    db = SessionLocal()
    try:
        return db.query(Dogovor).get(dogovor_id)
    finally:
        db.close()