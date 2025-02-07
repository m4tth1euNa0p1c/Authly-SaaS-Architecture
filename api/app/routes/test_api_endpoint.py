from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, text
import firebase_admin
from app.config.settings import settings
from app.core.firebase import verify_firebase_token
from app.core.database import SessionLocal

router = APIRouter()

@router.get("/firebase-test", summary="Test Firebase Connection")
def firebase_test():
    try:
        app_firebase = firebase_admin.get_app()
        return {
            "status": "success",
            "message": "Firebase is connected",
            "firebase_app": app_firebase.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firebase is not connected: {str(e)}")

@router.get("/config", summary="Get Configuration")
def get_config():
    return {
        "host": settings.host,
        "port": settings.port,
        "debug": settings.debug,
        "database_url": settings.database_url,
        "secret_key": settings.secret_key,
        "algorithm": settings.algorithm,
        "access_token_expire_minutes": settings.access_token_expire_minutes,
        "google_client_id": settings.google_client_id,
        "google_client_secret": settings.google_client_secret,
        "firebase_service_account_path": settings.firebase_service_account_path
    }

@router.get("/hello-world", summary="Hello World Endpoint")
def hello_world():
    return {"message": "Hello World"}

@router.get("/db/test/admin", summary="Test DB: Get Admin Info")
def get_admin_info():
    engine = create_engine(settings.database_url)
    query = text("""
        SELECT 
            u.id AS user_id,
            u.email,
            u.first_name,
            u.last_name,
            u.is_active,
            u.created_at,
            u.updated_at,
            r.id AS role_id,
            r.name AS role_name,
            r.description AS role_description
        FROM authly.users u
        LEFT JOIN authly.user_roles ur ON u.id = ur.user_id
        LEFT JOIN authly.roles r ON ur.role_id = r.id
        WHERE u.email = :email
    """)
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {"email": "testadmin@example.com"})
            rows = result.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail="Aucun administrateur trouvé.")
            return [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des infos admin: {str(e)}")

@router.get("/db/test/users", summary="Test DB: Get All Users")
def get_all_users():
    db: Session = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM authly.users"))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des utilisateurs: {str(e)}")
    finally:
        db.close()