from app.database.session import SessionLocal
from app.models.user import User

def verify_user(email: str):
    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    user.is_verified = True

    db.commit()
    db.close()

def make_admin(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    user.role = "admin"
    db.commit()
    db.close()