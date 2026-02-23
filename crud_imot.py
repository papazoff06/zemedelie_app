from sqlalchemy.orm import Session
from database import SessionLocal
from models import Imot, VidImot, NTP

def create_imot(
    ecatte: str,
    imot_nomer: str,
    obshta_plosht: float,
    plosht_sobstvena: float | None,
    plosht_naeta: float | None,
    vid: VidImot,
    ntp: NTP,
    mestnost: str | None = None,
    kategoriya: str | None = None,
    zabelezhka: str | None = None
):
    db: Session = SessionLocal()
    try:
        imot = Imot(
            ecatte=ecatte,
            imot_nomer=imot_nomer,
            obshta_plosht=obshta_plosht,
            plosht_sobstvena=plosht_sobstvena,
            plosht_naeta=plosht_naeta,
            vid=vid,
            ntp=ntp,
            mestnost=mestnost,
            kategoriya=kategoriya,
            zabelezhka=zabelezhka
        )
        db.add(imot)
        db.commit()
        db.refresh(imot)
        return imot
    finally:
        db.close()


def get_imot_by_nomer(imot_nomer: str):
    db = SessionLocal()
    try:
        return db.query(Imot).filter(Imot.imot_nomer == imot_nomer).first()
    finally:
        db.close()