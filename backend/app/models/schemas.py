"""Pydantic schemas for NetworkCellularMap v2.0"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class NetworkRole(str, Enum):
    """Network role classification"""
    HUB = "hub"
    CONNECTOR = "connector"
    LEAF = "leaf"
    REGULATOR = "regulator"


class RelationType(str, Enum):
    """Edge relationship types"""
    PPI = "PPI"
    REGULATES = "REGULATES"
    METABOLIC = "METABOLIC"
    VIRAL_HOST = "VIRAL_HOST"


class MutationStatus(str, Enum):
    """Mutation status"""
    WT = "wt"
    HET = "het"
    HOM = "hom"


class GenomePosition(BaseModel):
    """Genomic position information"""
    chr: str = Field(..., description="Chromosome")
    pos: int = Field(..., description="Position")
    ref: str = Field(..., description="Reference allele")
    alt: str = Field(..., description="Alternate allele")


class CellAgnosticNode(BaseModel):
    """Universal node present in all cells"""
    universal_id: str = Field(..., description="Unique identifier across all cells")
    genome_position: Optional[GenomePosition] = None
    present_in_all_cells: bool = True
    network_role: NetworkRole
    mutation_status: MutationStatus = MutationStatus.WT
    expression_all_cells: List[float] = Field(default_factory=list)
    hub_gravity: float = Field(0.0, ge=0.0, le=1.0)
    organ_agnostic_impact: float = Field(0.0, ge=-1.0, le=1.0)


class PanCellularEdge(BaseModel):
    """Universal edge relationship"""
    source_id: str
    target_id: str
    relation_type: RelationType
    exists_in_all_cells: bool = True
    disruption_impact: float = Field(0.0, ge=-1.0, le=1.0)
    weight: float = Field(1.0, ge=0.0)


class CodexScores(BaseModel):
    """Codex metric scores"""
    trueness: float = Field(..., ge=0.0, le=1.0, description="Pan-cellular restoration score")
    flow: float = Field(..., ge=0.0, le=1.0, description="Universal delivery score")
    gravity: float = Field(..., ge=0.0, le=1.0, description="Universal hub score")


class UniversalHub(BaseModel):
    """Universal hub information"""
    hub_id: str
    universal_degree_centrality: float
    betweenness_centrality: float
    eigenvector_centrality: float
    tissues: List[str]
    gravity_score: float
    codex_scores: Optional[CodexScores] = None


class CrisprPayload(BaseModel):
    """CRISPR-Cas9 payload design"""
    target_id: str
    grna_sequence: str = Field(..., max_length=20, description="Guide RNA sequence (up to 20 nucleotides)")
    hdr_template: str
    delivery_vector: str = "AAV9_multitropic"
    predicted_efficiency: float = Field(..., ge=0.0, le=1.0)


class DiseaseModule(BaseModel):
    """Disease module information"""
    module_id: str
    affected_tissues: List[str]
    hub_nodes: List[str]
    dysfunction_score: float = Field(..., ge=0.0, le=1.0)
    causal_mutations: List[str]


class DiagnosisRequest(BaseModel):
    """Diagnosis request input"""
    patient_genome: Dict[str, GenomePosition]
    symptoms_multi_organ: List[str]
    patient_id: Optional[str] = None


class DiagnosisResponse(BaseModel):
    """Diagnosis response output"""
    patient_id: Optional[str] = None
    network_dysfunction: List[DiseaseModule]
    universal_targets: List[UniversalHub]
    codex_scores: CodexScores
    recommended_interventions: List[CrisprPayload]


class RepairDesignRequest(BaseModel):
    """Repair design request"""
    hub_id: str
    mutation_ids: List[str]
    target_tissues: Optional[List[str]] = None


class RepairDesignResponse(BaseModel):
    """Repair design response with bill of materials"""
    hub_id: str
    crispr_payload: CrisprPayload
    aav9_vector: Dict[str, Any]
    validation_results: Dict[str, float]
    estimated_success_rate: float
