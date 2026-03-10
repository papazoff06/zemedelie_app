from database import SessionLocal
from models import PravoImot


def create_pravo_imot(
    imot_id,
    dokument_id,
    tip_pravo,
    plosht_pravo,
    data_nachalo,
    data_krai=None,
    cena_na_dka=None,
    zabelezhka=None
):
    session = SessionLocal()

    pravo = PravoImot(
        imot_id=imot_id,
        dokument_id=dokument_id,
        tip_pravo=tip_pravo,
        plosht_pravo=plosht_pravo,
        cena_na_dka=cena_na_dka,
        data_nachalo=data_nachalo,
        data_krai=data_krai,
        zabelezhka=zabelezhka
    )

    session.add(pravo)
    session.commit()
    session.refresh(pravo)
    session.close()

    return pravo



def dokumenti_za_imot(imot_id):
    session = SessionLocal()

    prava = (
        session.query(PravoImot)
        .filter(PravoImot.imot_id == imot_id)
        .all()
    )

    session.close()
    return prava


def obshta_plosht_po_dogovor(dokument_id):

    session = SessionLocal()

    prava = (
        session.query(PravoImot)
        .filter(PravoImot.dokument_id == dokument_id)
        .all()
    )

    total = sum(p.plosht_pravo for p in prava)

    session.close()

    return total


def prava_po_dogovor(dokument_id):

    session = SessionLocal()

    prava = (
        session.query(PravoImot)
        .filter(PravoImot.dokument_id == dokument_id)
        .all()
    )

    session.close()

    return prava