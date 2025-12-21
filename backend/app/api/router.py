"""Main API router"""
from fastapi import APIRouter
from .endpoints import networkologist, universal_hub, repair_design, tapspeak, cerebro

api_router = APIRouter()

api_router.include_router(
    networkologist.router,
    prefix="/networkologist",
    tags=["networkologist"]
)

api_router.include_router(
    universal_hub.router,
    prefix="/universal_hub",
    tags=["universal_hub"]
)

api_router.include_router(
    repair_design.router,
    prefix="/repair_design",
    tags=["repair_design"]
)

api_router.include_router(
    tapspeak.router,
    prefix="/tapspeak",
    tags=["tapspeak"]
)

api_router.include_router(
    cerebro.router,
    tags=["cerebro"]
)
