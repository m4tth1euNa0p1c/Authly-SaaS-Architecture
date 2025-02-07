from fastapi import APIRouter, HTTPException, Header, Query
from app.schemas import auth_schemas
from app.services import auth_service

router = APIRouter()

@router.post("/login", response_model=auth_schemas.LoginResponse, summary="User Login")
def login(request: auth_schemas.LoginRequest):
    token_data = auth_service.login(request)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid credentials or Firebase token")
    return token_data

@router.post("/logout", summary="User Logout")
def logout(authorization: str = Header(...)):
    try:
        auth_service.logout(authorization)
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh", response_model=auth_schemas.RefreshResponse, summary="Refresh Token")
def refresh(request: auth_schemas.RefreshRequest):
    new_token = auth_service.refresh_token(request.refresh_token)
    if not new_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return new_token

@router.get("/oauth/{provider}", summary="OAuth Redirect")
def oauth_redirect(provider: str):
    try:
        redirect_url = auth_service.get_oauth_redirect(provider)
        return {"redirect_url": redirect_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/verify-email", response_model=auth_schemas.RegisterResponse, summary="Email Verification")
def verify_email(token: str = Query(...)):
    try:
        response = auth_service.verify_email(token)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/finalize", response_model=auth_schemas.RegisterResponse, summary="Finalize Registration")
def finalize_registration(request: auth_schemas.RegisterRequest, authorization: str = Header(...)):
    try:
        result = auth_service.finalize_registration(request, authorization)
        return result
    except Exception as e:
        # Log the error for debugging
        print(f"Erreur /auth/finalize: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/register", summary="User Registration", response_model=dict)
def register(request: auth_schemas.RegisterRequest):
    try:
        response = auth_service.register(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
