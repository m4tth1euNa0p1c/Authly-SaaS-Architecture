from sqlalchemy.orm import Session
from app.models.user import User
from datetime import datetime

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict) -> User:
    user = User(
        email=user_data["email"],
        hashed_password=user_data["password"],
        first_name=user_data.get("first_name", ""),
        last_name=user_data.get("last_name", ""),
        email_verified=user_data.get("email_verified", False)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_email_verified(db: Session, user: User, verified: bool = True) -> User:
    user.email_verified = verified
    db.commit()
    db.refresh(user)
    return user

def update_last_login(db: Session, user: User) -> User:
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user