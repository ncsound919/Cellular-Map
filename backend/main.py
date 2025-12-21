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
    print("\n" + "="*60)
    print("🧠 NetworkCellularMap v2.0 + Cerebro.Networkology")
    print("="*60)
    print("\nInitializing systems...")
    
    # Database initialization
    try:
        db_connection.connect()
        db_connection.initialize_schema()
        print("✓ Database connected and schema initialized")
    except Exception as e:
        print(f"⚠ Database connection failed: {e}")
        print("  Application requires database connection. Please check Neo4j configuration.")
        # For production, uncomment the line below to fail fast:
        # raise
    
    # Cerebro initialization
    try:
        from app.services.cerebro import initialize_cerebro
        cerebro = await initialize_cerebro({
            "name": "Networkologist",
            "field": "Biotech"
        })
        print("\n🧠 Cerebro.Networkology - Big dogs eat first")
        print("   - SpatialGCN loaded ✓")
        print("   - TapSpeak active ✓")
        print("   - Autonomous agent: Running ✓")
        print("   - Learning from your patterns...")
        
        # Safely access cognitive profile
        cognitive_profile = getattr(cerebro, "cognitive_profile", None)
        if isinstance(cognitive_profile, dict) and "style" in cognitive_profile:
            print(f"   - Cognitive profile: {cognitive_profile['style']}")
        
        print("\n   Ready to explore networkology!\n")
    except Exception as e:
        print(f"⚠ Cerebro initialization failed: {e}")
        print("  Cerebro-related features may be unavailable or limited for this session.")
    
    print("="*60 + "\n")
    
    yield
    
    # Shutdown
    print("\nShutting down NetworkCellularMap v2.0...")
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
        "cerebro": {
            "enabled": True,
            "tagline": "Big dogs eat first - Autonomous networkologist copilot",
            "features": [
                "Autonomous agent (works 24/7)",
                "Cognitive personalization",
                "Real-time copilot",
                "Predictive intelligence",
                "TapSpeak translation"
            ]
        },
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
