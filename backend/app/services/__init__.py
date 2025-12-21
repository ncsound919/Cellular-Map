"""Services initialization"""

from .ingestion import DataIngestionService, OMIMService, GenBankService, KEGGService
from .network import UniversalInteractomeService
from .ai_scientist import CausalDiscoveryService, NetworkVulnerabilityService
from .codex import CodexMetricsService
from .repair import RepairDesignService
from .spatial_omics import SpatialOmicsService
from .federated_learning import FederatedLearningService
from .orchestration import (
    NetworkologyPipeline,
    NetworkologyDAG,
    TapSpeakGenerator,
    BBTechMetrics
)
from .cerebro import CerebroCore, get_cerebro, initialize_cerebro

__all__ = [
    # Core services
    "DataIngestionService",
    "OMIMService",
    "GenBankService",
    "KEGGService",
    "UniversalInteractomeService",
    "CausalDiscoveryService",
    "NetworkVulnerabilityService",
    "CodexMetricsService",
    "RepairDesignService",
    # Composable toolchain services
    "SpatialOmicsService",
    "FederatedLearningService",
    "NetworkologyPipeline",
    "NetworkologyDAG",
    "TapSpeakGenerator",
    "BBTechMetrics",
    # Cerebro autonomous agent
    "CerebroCore",
    "get_cerebro",
    "initialize_cerebro",
]
