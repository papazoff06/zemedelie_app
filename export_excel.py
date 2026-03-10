from openpyxl import Workbook
from database import SessionLocal
from models import Dokument, PravoImot, Imot


def export_renti_excel(filepath="rent_report.xlsx"):

    session = SessionLocal()

    wb = Workbook()
    ws = wb.active
    ws.title = "Ренти"

    # header
    ws.append([
        "№ договор",
        "Дата",
        "Наемодател",
        "ЕГН/Булстат",
        "ЕКАТТЕ",
        "Имот",
        "Площ (дка)",
        "Цена €/дка",
        "Сума €"
    ])

    dokumenti = session.query(Dokument).all()

    for d in dokumenti:

        prava = (
            session.query(PravoImot)
            .filter(PravoImot.dokument_id == d.id)
            .all()
        )

        for p in prava:

            imot = session.get(Imot, p.imot_id)

            cena = p.cena_na_dka or 0
            suma = p.plosht_pravo * cena

            ws.append([
                d.nomer,
                str(d.data),
                d.naemodatel,
                d.egn_bulstat,
                imot.ecatte,
                imot.imot_nomer,
                p.plosht_pravo,
                cena,
                suma
            ])

    session.close()

    wb.save(filepath)