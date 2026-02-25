from database import SessionLocal
from models import Dokument


def create_dokument(
    nomer,
    data,
    tip,
    filepath,
    zabelezhka=None
):
    session = SessionLocal()

    dokument = Dokument(
        nomer=nomer,
        data=data,
        tip=tip,
        filepath=filepath,
        zabelezhka=zabelezhka
    )

    session.add(dokument)
    session.commit()
    session.refresh(dokument)
    session.close()

    return dokument