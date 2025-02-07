import jwt
from datetime import datetime, timedelta
from app.config.settings import settings

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except Exception as e:
        raise Exception(f"Token invalid: {str(e)}")
