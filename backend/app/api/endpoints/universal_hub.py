"""Universal hub analysis endpoint"""
from fastapi import APIRouter, HTTPException, Path
from typing import Dict, Any
from ...services.network import UniversalInteractomeService
from ...services.codex import CodexMetricsService

router = APIRouter()


@router.get("/{mutation_id}", response_model=Dict[str, Any])
async def get_universal_hub_analysis(
    mutation_id: str = Path(..., description="Universal mutation identifier")
):
    """
    Pan-cellular impact analysis for a specific mutation
    
    Returns comprehensive analysis of mutation impact across all cell types
    """
    try:
        network_service = UniversalInteractomeService()
        codex_service = CodexMetricsService()
        
        # Calculate network metrics
        gravity = network_service.calculate_hub_gravity(mutation_id)
        
        # Get disease module
        module_nodes = network_service.find_disease_module([mutation_id])
        
        # Simulate attack to assess criticality
        attack_results = network_service.simulate_hub_attack(removal_fraction=0.2)
        
        return {
            "mutation_id": mutation_id,
            "pan_cellular_impact": {
                "gravity_score": gravity,
                "affected_module_size": len(module_nodes),
                "module_nodes": module_nodes[:10],  # Top 10
                "network_criticality": "high" if attack_results["network_collapsed"] else "low"
            },
            "topology_analysis": {
                "hub_attack_vulnerability": attack_results,
                "scale_free_validation": network_service.validate_scale_free()
            },
            "tissues_affected": ["heart", "brain", "liver", "muscle"],  # All tissues
            "universal": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Universal hub analysis failed: {str(e)}"
        )


@router.get("/{mutation_id}/neighbors", response_model=Dict[str, Any])
async def get_hub_neighbors(
    mutation_id: str = Path(..., description="Universal mutation identifier")
):
    """Get neighboring nodes in the pan-cellular network"""
    try:
        network_service = UniversalInteractomeService()
        
        # Get direct neighbors
        if mutation_id in network_service.graph:
            neighbors = list(network_service.graph.neighbors(mutation_id))
            
            return {
                "mutation_id": mutation_id,
                "neighbor_count": len(neighbors),
                "neighbors": neighbors[:20],  # First 20
                "pan_cellular": True
            }
        else:
            return {
                "mutation_id": mutation_id,
                "error": "Node not found in network"
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve neighbors: {str(e)}"
        )
