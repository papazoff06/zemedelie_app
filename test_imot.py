from crud_imot import create_imot, get_imot_by_nomer
from models import VidImot, NTP

imot = create_imot(
    ecatte="12345",
    imot_nomer="12.345",
    obshta_plosht=5.0,
    plosht_sobstvena=3.0,
    plosht_naeta=2.0,
    vid=VidImot.sasobsven,
    ntp=NTP.niva,
    mestnost="Голямата мера",
    kategoriya="IV",
    zabelezhka="Тестов имот"
)

print("Създаден имот:", imot.imot_nomer)

found = get_imot_by_nomer("12.345")
print("Намерен имот:", found.imot_nomer)