"""
NetworkCellularMap v2.0 - Main FastAPI Application
Networkology Core Engine - Organ Agnostic Network Diagnosis
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.router import api_router
from app.db.neo4j import db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("Starting NetworkCellularMap v2.0...")
    try:
        db_connection.connect()
        db_connection.initialize_schema()
        print("Database connected and schema initialized")
    except Exception as e:
        print(f"CRITICAL: Database connection failed: {e}")
        print("Application requires database connection. Please check Neo4j configuration.")
        # For production, uncomment the line below to fail fast:
        # raise
    
    yield
    
    # Shutdown
    print("Shutting down NetworkCellularMap v2.0...")
    db_connection.close()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Networkology Core Engine - Organ Agnostic Network Diagnosis",
    lifespan=lifespan
)

# Configure CORS
# For development: allows localhost. For production: set ALLOWED_ORIGINS environment variable
allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
if hasattr(settings, 'ALLOWED_ORIGINS') and settings.ALLOWED_ORIGINS:
    allowed_origins = settings.ALLOWED_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "NetworkCellularMap",
        "version": "2.0",
        "paradigm": "organ_agnostic_network_diagnosis",
        "core_principle": "Single mutation propagates across all cells; target network dysfunction not organ symptoms",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    db_status = "disconnected"
    try:
        # Check database connection
        db_connection.execute_query("RETURN 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    overall_status = "healthy" if db_status == "connected" else "unhealthy"
    
    return {
        "status": overall_status,
        "version": settings.VERSION,
        "services": {
            "api": "running",
            "database": db_status
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
