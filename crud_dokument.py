from database import SessionLocal
from models import Dokument


def create_dokument(
    nomer,
    data,
    tip,
    naemodatel=None,
    egn_bulstat=None,
    filepath="",
    zabelezhka=None
):
    session = SessionLocal()

    dokument = Dokument(
        nomer=nomer,
        data=data,
        tip=tip,
        filepath=filepath,
        naemodatel=naemodatel,
        egn_bulstat=egn_bulstat,
        zabelezhka=zabelezhka
    )

    session.add(dokument)
    session.commit()
    session.refresh(dokument)
    session.close()

    return dokument


def get_all_dokumenti():
    session = SessionLocal()

    dokumenti = (
        session.query(Dokument)
        .order_by(Dokument.data.desc())
        .all()
    )

    session.close()

    return dokumenti