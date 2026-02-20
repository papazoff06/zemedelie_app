from database import SessionLocal
from models import Imot, Deklarator, DeklaratorImot

session = SessionLocal()

# 1️⃣ create deklarator
deklarator = Deklarator(
    ime="Anton Ivanov",
    egn="9001010000",
    telefon="0888123456"
)

session.add(deklarator)
session.commit()

# 2️⃣ create imot
imot = Imot(
    imot_nomer="12345",
    plosht=25.5,
    vid="sobstven",
    procent=100
)

session.add(imot)
session.commit()

# 3️⃣ link deklarator <-> imot
link = DeklaratorImot(
    deklarator_id=deklarator.id,
    imot_id=imot.id
)

session.add(link)
session.commit()

session.close()

print("Test data inserted successfully")
