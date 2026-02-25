from database import SessionLocal
from models import Imot


def create_imot(
    ecatte,
    imot_nomer,
    plosht_kadastr,
    ntp,
    kategoriya=None,
    mestnost=None,
    zabelezhka=None
):
    session = SessionLocal()

    imot = Imot(
        ecatte=ecatte,
        imot_nomer=imot_nomer,
        plosht_kadastr=plosht_kadastr,
        ntp=ntp,
        kategoriya=kategoriya,
        mestnost=mestnost,
        zabelezhka=zabelezhka
    )

    session.add(imot)
    session.commit()
    session.refresh(imot)
    session.close()

    return imot


def get_imot_by_nomer(ecatte, imot_nomer):
    session = SessionLocal()

    imot = (
        session.query(Imot)
        .filter_by(ecatte=ecatte, imot_nomer=imot_nomer)
        .first()
    )

    session.close()
    return imot