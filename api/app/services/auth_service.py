# app/services/auth_service.py
import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.schemas import auth_schemas
from app.core.security import create_access_token, verify_access_token
from app.core.firebase import verify_firebase_token
from app.repositories import user_repository
from app.core.database import SessionLocal
from app.config.settings import settings
import logging

# Configure logging (production should use a proper logging configuration)
logger = logging.getLogger("auth_service")
logger.setLevel(logging.INFO)

EMAIL_VERIFICATION_SECRET = settings.secret_key
EMAIL_VERIFICATION_EXPIRE_MINUTES = 15

def generate_email_verification_token(register_data: dict) -> str:
    payload = register_data.copy()
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=EMAIL_VERIFICATION_EXPIRE_MINUTES)})
    return jwt.encode(payload, EMAIL_VERIFICATION_SECRET, algorithm=settings.algorithm)

def verify_email_verification_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, EMAIL_VERIFICATION_SECRET, algorithms=[settings.algorithm])
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Le token de vérification a expiré.")
    except jwt.JWTError as e:
        raise Exception(f"Token de vérification invalide: {str(e)}")

def register(request: auth_schemas.RegisterRequest) -> dict:
    db = SessionLocal()
    try:
        if user_repository.get_user_by_email(db, request.email):
            raise Exception("Un utilisateur avec cet email existe déjà.")

        register_data = {
            "email": request.email,
            "password": bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            "first_name": request.first_name or "",
            "last_name": request.last_name or ""
        }
        verification_token = generate_email_verification_token(register_data)
        verification_link = f"{settings.api_base_url}/auth/verify-email?token={verification_token}"
        logger.info(f"[EMAIL VERIFICATION] Lien: {verification_link}")
        return {"message": "Un e-mail de vérification a été envoyé (flux custom)."}
    finally:
        db.close()

def verify_email(token: str) -> auth_schemas.RegisterResponse:
    registration_data = verify_email_verification_token(token)
    db = SessionLocal()
    try:
        if user_repository.get_user_by_email(db, registration_data["email"]):
            raise Exception("Cet utilisateur est déjà enregistré.")
        registration_data["first_name"] = registration_data.get("first_name", "")
        registration_data["last_name"] = registration_data.get("last_name", "")
        user = user_repository.create_user(db, {
            "email": registration_data["email"],
            "password": registration_data["password"],
            "first_name": registration_data["first_name"],
            "last_name": registration_data["last_name"],
            "email_verified": True
        })
        logger.info(f"User created: {user.email} (verified: {user.email_verified})")
        access_token = create_access_token({"sub": registration_data["email"]})
        expires_in = settings.access_token_expire_minutes * 60
        refresh_token = "dummy_refresh_token_register"
        return auth_schemas.RegisterResponse(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token
        )
    finally:
        db.close()

def finalize_registration(request: auth_schemas.RegisterRequest, authorization: str) -> auth_schemas.RegisterResponse:
    if not authorization.startswith("Bearer "):
        raise Exception("En-tête Authorization invalide ou absent.")
    id_token = authorization.split(" ")[1]
    decoded = verify_firebase_token(id_token)
    firebase_email = decoded.get("email")
    if not firebase_email:
        raise Exception("Le token Firebase ne contient pas d'email.")
    if firebase_email.lower() != request.email.lower():
        raise Exception("Le token Firebase ne correspond pas à l'email fourni.")

    db = SessionLocal()
    try:
        if user_repository.get_user_by_email(db, request.email):
            raise Exception("Cet utilisateur est déjà enregistré.")

        hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_data = {
            "email": request.email,
            "password": hashed_password,
            "first_name": request.first_name or "",
            "last_name": request.last_name or "",
            "email_verified": True
        }
        created_user = user_repository.create_user(db, user_data)
        logger.info(f"User created via finalize: {created_user.email}, verified={created_user.email_verified}")
        access_token = create_access_token({"sub": request.email})
        expires_in = settings.access_token_expire_minutes * 60
        refresh_token = "dummy_refresh_token_register"
        return auth_schemas.RegisterResponse(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token
        )
    finally:
        db.close()

def login(request: auth_schemas.LoginRequest) -> auth_schemas.LoginResponse:
    db = SessionLocal()
    try:
        user = None

        if request.firebase_token:
            try:
                decoded = verify_firebase_token(request.firebase_token)
                firebase_email = decoded.get("email")
                if not firebase_email or firebase_email.lower() != request.email.lower():
                    raise HTTPException(
                        status_code=401,
                        detail="Le token Firebase ne correspond pas à l'email fourni."
                    )
                user = user_repository.get_user_by_email(db, request.email)
                if not user:
                    raise HTTPException(
                        status_code=404,
                        detail="Utilisateur non trouvé pour ce token Firebase."
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=401,
                    detail=f"Échec de la validation du token Firebase : {str(e)}"
                )
        else:
            user = user_repository.get_user_by_email(db, request.email)
            if not user:
                raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
            if not bcrypt.checkpw(request.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
                raise HTTPException(status_code=401, detail="Mot de passe incorrect.")

        user_repository.update_last_login(db, user)
        access_token = create_access_token({"sub": user.email})
        expires_in = settings.access_token_expire_minutes * 60
        refresh_token = "dummy_refresh_token_admin"

        return auth_schemas.LoginResponse(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token
        )
    finally:
        db.close()

def logout(token: str):
    if token.startswith("Bearer "):
        token = token[7:]
    try:
        verify_access_token(token)
    except Exception as e:
        logger.warning(f"Logout: token verification failed: {e}")
    return True

def refresh_token(refresh_token: str) -> auth_schemas.RefreshResponse:
    if refresh_token == "dummy_refresh_token_admin":
        new_access_token = create_access_token({"sub": "testadmin@example.com"})
        expires_in = settings.access_token_expire_minutes * 60
        return auth_schemas.RefreshResponse(
            access_token=new_access_token,
            expires_in=expires_in
        )
    return None

def get_oauth_redirect(provider: str) -> str:
    provider = provider.lower()
    if provider == "google":
        return "https://accounts.google.com/o/oauth2/auth?client_id=your_client_id&redirect_uri=your_redirect_uri"
    elif provider == "github":
        return "https://github.com/login/oauth/authorize?client_id=your_client_id&redirect_uri=your_redirect_uri"
    elif provider == "facebook":
        return "https://www.facebook.com/v10.0/dialog/oauth?client_id=your_client_id&redirect_uri=your_redirect_uri"
    else:
        raise Exception("Provider not supported")
