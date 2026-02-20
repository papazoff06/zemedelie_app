from database import SessionLocal
from models import Imot

def get_imot_by_nomer(nomer):
    session = SessionLocal()
    imot = session.query(Imot).filter_by(imot_nomer=nomer).first()
    session.close()
    return imot


def create_imot(imot_nomer, plosht, vid, procent):
    session = SessionLocal()

    imot = Imot(
        imot_nomer=imot_nomer,
        plosht=plosht,
        vid=vid,
        procent=procent
    )

    session.add(imot)
    session.commit()
    session.close()
