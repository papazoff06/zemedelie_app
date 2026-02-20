from database import SessionLocal
from models import Imot

session = SessionLocal()

imot = session.query(Imot).filter_by(imot_nomer="12345").first()

print(imot.imot_nomer, imot.plosht, imot.vid)

session.close()
