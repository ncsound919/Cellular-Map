"""
TapSpeak API Endpoints for NetworkCellularMap v2.0

Endpoints for accessing the TapSpeak translation engine:
- Translate technical terms to plain English
- Search translations by tags or query
- Get dashboard data
- Validate translations
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ...models.schemas import (
    TapSpeakTranslation,
    BBTechMapping,
    TapSpeakCategory,
    TapSpeakSearchRequest,
    TapSpeakTranslateRequest,
    TapSpeakValidationRequest,
    TapSpeakDashboardData
)
from ...services.tapspeak import get_tapspeak_engine

router = APIRouter()


@router.get("/concepts", response_model=List[TapSpeakTranslation])
async def get_concepts(
    category: Optional[TapSpeakCategory] = Query(None, description="Filter by category")
):
    """
    Get all TapSpeak concepts, optionally filtered by category
    
    Categories:
    - core_concepts: Core biotech + networkology concepts
    - networkology_workflow: Workflow step translations
    - codex_translations: Codex metric translations
    """
    engine = get_tapspeak_engine()
    return engine.get_all_concepts(category)


@router.get("/bbtech", response_model=List[BBTechMapping])
async def get_bbtech_mappings():
    """
    Get Basketball-Biotech bridge mappings
    
    Returns all BBTech analogies that map basketball stats to biotech concepts.
    """
    engine = get_tapspeak_engine()
    return engine.get_bbtech_mappings()


@router.post("/search", response_model=List[TapSpeakTranslation])
async def search_translations(request: TapSpeakSearchRequest):
    """
    Search TapSpeak translations
    
    Search by:
    - Query text (searches tap_speak, professional, hooks, tags)
    - Tags (filter by specific tags)
    - Category (filter by category)
    - Confidence thresholds (minimum ESAT/CEP scores)
    
    Example queries:
    - "hub" - finds all hub-related translations
    - "crispr" - finds CRISPR-related concepts
    - "basketball" - finds all BBTech analogies
    """
    engine = get_tapspeak_engine()
    
    results = engine.search(
        query=request.query,
        tags=request.tags,
        min_esat=request.min_esat,
        min_cep=request.min_cep
    )
    
    # Filter by category if specified
    if request.category:
        category_concepts = engine.get_all_concepts(request.category)
        results = [r for r in results if r in category_concepts]
    
    return results


@router.post("/translate", response_model=Optional[TapSpeakTranslation])
async def translate_term(request: TapSpeakTranslateRequest):
    """
    Translate a technical term to TapSpeak
    
    Takes a technical biotech/networkology term and returns its TapSpeak translation
    with basketball analogy, mnemonic hooks, and plain English explanation.
    
    Example terms:
    - "Hub centrality"
    - "CRISPR-Cas9"
    - "Spatial transcriptomics"
    - "MC4R mutation"
    """
    engine = get_tapspeak_engine()
    
    translation = engine.translate_term(request.technical_term, request.domain)
    
    if not translation:
        raise HTTPException(
            status_code=404,
            detail=f"No TapSpeak translation found for '{request.technical_term}'. "
                   f"Consider adding it to the TapSpeak knowledge base."
        )
    
    return translation


@router.post("/validate")
async def validate_translation(request: TapSpeakValidationRequest):
    """
    Validate a TapSpeak translation quality
    
    Checks:
    - Confidence thresholds (ESAT >= 70, CEP >= 80)
    - TapSpeak phrase length (should be short)
    - Mnemonic hook quality
    - Tag completeness
    
    Returns validation results with issues and suggestions.
    """
    engine = get_tapspeak_engine()
    
    validation = engine.validate_translation(request.translation)
    
    return {
        "valid": validation["valid"],
        "issues": validation["issues"],
        "suggestions": validation["suggestions"],
        "translation_id": request.translation.id,
        "confidence": {
            "esat": request.translation.confidence.esat,
            "cep": request.translation.confidence.cep
        }
    }


@router.get("/dashboard", response_model=TapSpeakDashboardData)
async def get_dashboard_data():
    """
    Get complete TapSpeak dashboard data
    
    Returns all concepts, workflows, codex metrics, and BBTech mappings
    in a single response for dashboard rendering.
    
    Use this endpoint to populate the TapSpeak frontend dashboard.
    """
    engine = get_tapspeak_engine()
    return engine.get_dashboard_data()


@router.get("/concept/{concept_id}", response_model=TapSpeakTranslation)
async def get_concept_by_id(concept_id: int):
    """
    Get a specific TapSpeak concept by ID
    
    IDs:
    - 1-5: Core concepts
    - 10-14: Networkology workflow
    - 20-22: Codex translations
    """
    engine = get_tapspeak_engine()
    
    # Search through all translations
    for translation in engine._all_translations:
        if translation.id == concept_id:
            return translation
    
    raise HTTPException(
        status_code=404,
        detail=f"TapSpeak concept with ID {concept_id} not found"
    )


@router.get("/tags", response_model=List[str])
async def get_all_tags():
    """
    Get all available tags for filtering
    
    Returns a list of all unique tags used across all TapSpeak translations.
    Useful for building tag filters in the UI.
    """
    engine = get_tapspeak_engine()
    return sorted(engine._tag_index.keys())


@router.get("/stats")
async def get_statistics():
    """
    Get TapSpeak translation statistics
    
    Returns:
    - Total translations count
    - Average confidence scores
    - Translations by category
    - Tag distribution
    """
    engine = get_tapspeak_engine()
    dashboard = engine.get_dashboard_data()
    
    return {
        "total_translations": dashboard.total_translations,
        "average_confidence": {
            "esat": dashboard.average_confidence.esat,
            "cep": dashboard.average_confidence.cep
        },
        "by_category": {
            "core_concepts": len(dashboard.core_concepts),
            "networkology_workflow": len(dashboard.workflow_steps),
            "codex_translations": len(dashboard.codex_metrics),
            "bbtech_mappings": len(dashboard.bbtech_mappings)
        },
        "total_tags": len(engine._tag_index),
        "tags": sorted(engine._tag_index.keys())
    }
