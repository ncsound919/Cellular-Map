"""
Cerebro API Endpoints
Autonomous Networkologist Copilot
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from ...models.schemas import (
    CerebroUserProfile,
    CerebroQuery,
    CerebroResponse,
    CerebroReport,
    CerebroStatus
)
from ...services.cerebro import get_cerebro, initialize_cerebro

router = APIRouter(prefix="/cerebro", tags=["cerebro"])


@router.get("/status", response_model=CerebroStatus)
async def get_cerebro_status():
    """
    Get current Cerebro system status
    
    Returns initialization status, user profile, and agent status
    """
    cerebro = get_cerebro()
    return cerebro.get_status()


@router.post("/initialize")
async def initialize(user: Optional[CerebroUserProfile] = None):
    """
    Initialize Cerebro system with user profile
    
    Args:
        user: Optional user profile for personalization
        
    Returns:
        Initialization status and cognitive profile
    """
    user_dict = user.dict() if user is not None else None
    cerebro = await initialize_cerebro(user_dict)
    
    return {
        "status": "initialized",
        "message": "🧠 Cerebro.Networkology - Big dogs eat first",
        "cognitive_profile": cerebro.cognitive_profile,
        "agent_running": cerebro.agent.running
    }


@router.post("/personalize")
async def personalize_cerebro():
    """
    Personalize Cerebro to user's cognitive style
    
    Analyzes interaction patterns and adapts interface
    """
    cerebro = get_cerebro()
    
    if not cerebro.initialized:
        raise HTTPException(
            status_code=400,
            detail="Cerebro not initialized. Call /initialize first."
        )
    
    await cerebro.personalize()
    
    return {
        "status": "personalized",
        "cognitive_profile": cerebro.cognitive_profile,
        "message": f"✓ Personalized to: {cerebro.cognitive_profile['style']}"
    }


@router.post("/process_query", response_model=CerebroResponse)
async def process_query(query: CerebroQuery):
    """
    Process query with full Cerebro capabilities
    
    Args:
        query: User query with text and optional context
        
    Returns:
        Enhanced response with copilot insights and predictions
    """
    cerebro = get_cerebro()
    
    if not cerebro.initialized:
        raise HTTPException(
            status_code=400,
            detail="Cerebro not initialized. Call /initialize first."
        )
    
    # Process query
    result = await cerebro.process_query(query.dict())
    
    # Format response
    response = CerebroResponse(
        query=query,
        response=result,
        copilot_insights=result.get("copilot_thoughts", {}).get("suggestions", []),
        tap_speak=result.get("tap_speak"),
        predicted_next=[],
        status=result.get("status", "success")
    )
    
    return response


@router.get("/nightly_report", response_model=CerebroReport)
async def get_nightly_report():
    """
    Get autonomous agent's nightly report
    
    Returns:
        Daily discoveries, papers, patterns, and agenda
    """
    cerebro = get_cerebro()
    
    if not cerebro.initialized:
        raise HTTPException(
            status_code=400,
            detail="Cerebro not initialized. Call /initialize first."
        )
    
    report_data = await cerebro.nightly_report()
    
    # Format as CerebroReport
    report = CerebroReport(
        title=report_data["title"],
        date=report_data["title"].split(" - ")[-1],
        sections=report_data["sections"],
        summary="Autonomous agent discoveries and agenda"
    )
    
    return report


@router.post("/interact")
async def interact(query: CerebroQuery):
    """
    Interactive session with Cerebro
    
    Real-time copilot thinking and feedback
    """
    cerebro = get_cerebro()
    
    if not cerebro.initialized:
        raise HTTPException(
            status_code=400,
            detail="Cerebro not initialized. Call /initialize first."
        )
    
    # Get copilot thoughts
    copilot_thoughts = await cerebro.copilot.think_alongside(query.dict())
    
    return {
        "status": "thinking",
        "copilot_thoughts": copilot_thoughts,
        "has_immediate_value": copilot_thoughts.get("has_immediate_value", False)
    }
