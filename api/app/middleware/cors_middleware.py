from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings

def setup_cors(app):
    origins = [
        "http://localhost:5173",                 # Dev domain
        "https://booga.com"      # Production domain
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
