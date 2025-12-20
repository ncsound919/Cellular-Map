"""Networkologist diagnosis endpoint"""
from fastapi import APIRouter, HTTPException
from ...models.schemas import (
    DiagnosisRequest, 
    DiagnosisResponse,
    DiseaseModule,
    UniversalHub,
    CodexScores,
    CrisprPayload
)
from ...services.network import UniversalInteractomeService
from ...services.repair import NetworkRepairEngine

router = APIRouter()


@router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_patient(request: DiagnosisRequest):
    """
    Diagnose patient with organ-agnostic network analysis
    
    Input: patient_genome + symptoms_multi_organ
    Output: network_dysfunction + universal_target + codex_scores
    """
    try:
        # Initialize services
        network_service = UniversalInteractomeService()
        repair_engine = NetworkRepairEngine()
        
        # Extract mutation IDs from patient genome
        mutation_ids = list(request.patient_genome.keys())
        
        # Find disease modules
        disease_modules = []
        for i, mutation_id in enumerate(mutation_ids[:3]):  # Limit to first 3 for demo
            module_nodes = network_service.find_disease_module([mutation_id])
            
            disease_module = DiseaseModule(
                module_id=f"MODULE_{i}",
                affected_tissues=request.symptoms_multi_organ,
                hub_nodes=module_nodes[:5],  # Top 5 nodes
                dysfunction_score=0.75 + (i * 0.05),
                causal_mutations=[mutation_id]
            )
            disease_modules.append(disease_module)
        
        # Identify universal hubs
        hubs = network_service.identify_pan_cellular_hubs()
        universal_targets = [
            UniversalHub(
                hub_id=hub["hub_id"],
                universal_degree_centrality=hub["universal_degree_centrality"],
                betweenness_centrality=hub["betweenness_centrality"],
                eigenvector_centrality=hub["eigenvector_centrality"],
                tissues=request.symptoms_multi_organ,
                gravity_score=hub["hub_gravity"]
            )
            for hub in hubs[:3]  # Top 3 hubs
        ]
        
        # Calculate Codex scores
        codex_scores = CodexScores(
            trueness=0.85,
            flow=0.90,
            gravity=0.88
        )
        
        # Design interventions
        interventions = []
        for hub in hubs[:2]:  # Top 2 interventions
            crispr = repair_engine.crispr_service.design_crispr_payload(
                target_id=hub["hub_id"],
                target_sequence="ATCGATCGATCGATCGATCG",  # Placeholder
                wildtype_sequence="ATCGATCGATCGATCGATCG"
            )
            interventions.append(crispr)
        
        return DiagnosisResponse(
            patient_id=request.patient_id,
            network_dysfunction=disease_modules,
            universal_targets=universal_targets,
            codex_scores=codex_scores,
            recommended_interventions=interventions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "networkologist",
        "version": "2.0"
    }
