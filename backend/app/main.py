from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.db.base_class import Base
from app.db.session import engine
from app import models  # Import all models to register them

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Set all CORS enabled origins
# In development, allow all origins for mobile apps (Expo, etc.)
# In production, use specific allowed origins
cors_origins = settings.BACKEND_CORS_ORIGINS
if not cors_origins or settings.ENVIRONMENT == "development":
    # Allow all origins in development (needed for mobile apps with various origins)
    # Use allow_origin_regex to match all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r".*",  # Allow all origins via regex
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Production: use specific allowed origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables on startup.
    """
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to CampusConnect API", "environment": settings.ENVIRONMENT}

app.include_router(api_router, prefix=settings.API_V1_STR)
