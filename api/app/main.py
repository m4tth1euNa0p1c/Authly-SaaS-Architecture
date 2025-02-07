from fastapi import FastAPI
from app.routes import auth_routes, test_api_endpoint
from app.middleware.cors_middleware import setup_cors

app = FastAPI(
    title="Authly – Authentification Universelle",
    description="API pour gérer l'authentification, les utilisateurs, les rôles et les permissions.",
    version="1.0.0"
)

setup_cors(app)

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(test_api_endpoint.router, prefix="/test", tags=["Test Endpoints"])

@app.get("/health", summary="Health Check", tags=["System"])
def health_check():
    return {"status": "ok"}
