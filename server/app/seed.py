from sqlalchemy.orm import Session
from .db.session import SessionLocal
from .models import User, UserRole
from .security import get_password_hash

def seed_admin(email: str = "admin@example.com", password: str = "Admin@123"):
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print("Admin user already exists")
            return
        user = User(email=email, password=get_password_hash(password), role=UserRole.admin)
        db.add(user)
        db.commit()
        print(f"Seeded admin user: {email} / {password}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
