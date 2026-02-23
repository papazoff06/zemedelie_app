from crud_naem import create_naem, dogovori_za_imot
from crud_imot import get_imot_by_nomer
from datetime import date

imot = get_imot_by_nomer("12.345")
if imot is None:
    raise Exception("Имотът не съществува. Пусни test_imot.py първо.")
naem = create_naem(
    imot_id=imot.id,
    dogovor_id=1,
    plosht_dka=2.0,
    cena_na_dka=80.0,
    data_nachalo=date(2024, 10, 1),
    data_krai=None,
    zabelezhka="Съсобственост – 2 дка"
)

print("Добавен ред в договор")

dogovori = dogovori_za_imot(imot.id)
for d in dogovori:
    print("Имотът участва в договор:", d.nomer)

