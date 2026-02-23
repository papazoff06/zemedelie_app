from crud_dogovor import create_dogovor
from datetime import date
import os

os.makedirs("data/dogovori", exist_ok=True)

dogovor = create_dogovor(
    nomer="A-001",
    data=date(2024, 10, 1),
    tip="аренда",
    filepath="data/dogovori/test.pdf",
    zabelezhka="Тестов договор"
)

print("Създаден договор:", dogovor.nomer)