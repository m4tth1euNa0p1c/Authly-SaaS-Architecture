# app/repositories/refresh_token_repository.py
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
from app.config.settings import settings

def create_refresh_token(db: Session, user_id: int) -> RefreshToken:

    token_value = secrets.token_urlsafe(64)
    expires_at = datetime.utcnow() + timedelta(days=7)
    refresh_token_obj = RefreshToken(
        user_id=user_id,
        refresh_token=token_value,
        expires_at=expires_at,
        revoked=False
    )
    db.add(refresh_token_obj)
    db.commit()
    db.refresh(refresh_token_obj)
    return refresh_token_obj

def get_refresh_token(db: Session, token: str) -> RefreshToken:
    return db.query(RefreshToken).filter(RefreshToken.refresh_token == token).first()

def revoke_refresh_token(db: Session, token: str) -> None:
    rt = get_refresh_token(db, token)
    if rt:
        rt.revoked = True
        rt.revoked_at = datetime.utcnow()
        db.commit()

def delete_refresh_tokens_for_user(db: Session, user_id: int) -> None:
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
    db.commit()
