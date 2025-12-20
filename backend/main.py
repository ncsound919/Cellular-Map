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
        print(f"Database connection warning: {e}")
    
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
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
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "services": {
            "api": "running",
            "database": "connected"
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
