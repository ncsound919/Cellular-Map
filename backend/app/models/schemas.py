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
    grna_sequence: str = Field(
        ..., 
        min_length=20, 
        max_length=20, 
        description="Guide RNA sequence (exactly 20 nucleotides for CRISPR-Cas9)"
    )
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


# ============================================================================
# TapSpeak Translation System Models
# ============================================================================

class ConfidenceMetrics(BaseModel):
    """Confidence metrics for TapSpeak translations"""
    esat: float = Field(..., ge=0.0, le=100.0, description="Everyday Speech Accuracy Threshold (0-100)")
    cep: float = Field(..., ge=0.0, le=100.0, description="Conceptual Equivalence Precision (0-100)")
    
    def meets_threshold(self, esat_min: float = 70.0, cep_min: float = 80.0) -> bool:
        """Check if confidence meets minimum thresholds"""
        return self.esat >= esat_min and self.cep >= cep_min


class TapSpeakTranslation(BaseModel):
    """Core TapSpeak translation with 7-layer structure"""
    id: int = Field(..., description="Sequential ID")
    tap_speak: str = Field(..., description="Plain English memorable hook")
    professional: str = Field(..., description="Technical term or metric")
    operational: str = Field(..., description="How it works mechanistically")
    translational: str = Field(..., description="Real-world impact for common man")
    confidence: ConfidenceMetrics
    hooks: str = Field(..., description="Mnemonic device for memory")
    tags: List[str] = Field(..., description="Searchable categories")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 5,
                "tap_speak": "Big dogs eat first (high Gravity)",
                "professional": "Hub centrality + attractiveness index",
                "operational": "Scale-free network hubs control 80% system state",
                "translational": "Fix the kingpin one shot cures whole disease",
                "confidence": {"esat": 90.0, "cep": 95.0},
                "hooks": "Elephant in room pulls whole circus",
                "tags": ["hubs", "achilles", "gravity", "codex"]
            }
        }


class BBTechMapping(BaseModel):
    """Basketball to Biotech translation mapping"""
    id: int
    tap_speak: str = Field(..., description="Basketball analogy phrase")
    professional: str = Field(..., description="Basketball stat")
    operational: str = Field(..., description="Biotech mechanism")
    translational: str = Field(..., description="Networkology meaning")
    confidence: ConfidenceMetrics
    hooks: str
    tags: List[str]


class TapSpeakCategory(str, Enum):
    """TapSpeak concept categories"""
    CORE_CONCEPTS = "core_concepts"
    NETWORKOLOGY_WORKFLOW = "networkology_workflow"
    CODEX_TRANSLATIONS = "codex_translations"
    BBTECH_BRIDGE = "basketball_biotech_bridge"


class TapSpeakSearchRequest(BaseModel):
    """Search request for TapSpeak translations"""
    query: Optional[str] = None
    category: Optional[TapSpeakCategory] = None
    tags: Optional[List[str]] = None
    min_esat: float = Field(70.0, ge=0.0, le=100.0)
    min_cep: float = Field(80.0, ge=0.0, le=100.0)


class TapSpeakTranslateRequest(BaseModel):
    """Request to translate a technical term"""
    technical_term: str = Field(..., description="Technical biotech term to translate")
    domain: str = Field("biotech", description="Domain (biotech, networkology, etc.)")
    context: Optional[str] = None


class TapSpeakValidationRequest(BaseModel):
    """Request to validate a TapSpeak translation"""
    translation: TapSpeakTranslation
    feedback: Optional[str] = None


class TapSpeakDashboardData(BaseModel):
    """TapSpeak dashboard data for frontend"""
    core_concepts: List[TapSpeakTranslation]
    workflow_steps: List[TapSpeakTranslation]
    codex_metrics: List[TapSpeakTranslation]
    bbtech_mappings: List[BBTechMapping]
    total_translations: int
    average_confidence: ConfidenceMetrics


# ===== Cerebro Models =====

class CerebroUserProfile(BaseModel):
    """User profile for Cerebro personalization"""
    name: str = Field(..., description="User name")
    field: str = Field(default="Biotech", description="Research field")
    cognitive_style: Optional[str] = Field(None, description="Detected cognitive style")
    preferences: Dict[str, Any] = Field(default_factory=dict)


class CerebroInputType(str, Enum):
    """Allowed input types for Cerebro queries"""
    TEXT = "text"
    VOICE = "voice"
    NEURAL = "neural"
    GESTURE = "gesture"


class CerebroQuery(BaseModel):
    """Query submitted to Cerebro"""
    text: str = Field(..., description="Query text")
    input_type: CerebroInputType = Field(
        default=CerebroInputType.TEXT,
        description="Input type: text, voice, neural, gesture"
    )
    context: Optional[Dict[str, Any]] = None


class CerebroResponse(BaseModel):
    """Response from Cerebro query processing"""
    query: CerebroQuery
    response: Dict[str, Any]
    copilot_insights: List[str] = Field(default_factory=list)
    tap_speak: Optional[str] = None
    predicted_next: List[str] = Field(default_factory=list)
    status: str = "success"


class CerebroReport(BaseModel):
    """Nightly report from autonomous agent"""
    title: str
    date: str
    sections: Dict[str, List[Any]]
    summary: Optional[str] = None


class CerebroStatus(BaseModel):
    """Current status of Cerebro system"""
    initialized: bool
    user: str
    cognitive_profile: Optional[str]
    agent_running: bool
    memory_size: int
    timestamp: str
