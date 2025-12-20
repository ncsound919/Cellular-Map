# Composable Toolchain Architecture

NetworkCellularMap v2.0 implements a **small, composable toolchain** with three distinct layers that avoid monolithic architecture and keep the Networkology + TapSpeak stack lean.

## Architecture Philosophy

The toolchain follows a modular approach:

```
┌─────────────────────────────────────────────────────────────┐
│               Composable Toolchain Stack                     │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Spatial / Network Core (lightweight)              │
│    • Scanpy + AnnData: Single-cell preprocessing            │
│    • Squidpy: Spatial neighborhood graphs                   │
│    • NetworkX: Prototype interactomes                        │
│    • Neo4j: Persistent network storage                      │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Training / AI (minimal but powerful)              │
│    • PyTorch: Core deep learning                            │
│    • PyTorch Geometric: GNN message passing                 │
│    • scvi-tools: Probabilistic single-cell models           │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Federated / Global Adoption                       │
│    • FedLab: Simulation-oriented FL                         │
│    • OpenFL: Production-grade federated learning            │
├─────────────────────────────────────────────────────────────┤
│  Orchestration: Without Bloat                               │
│    • NetworkologyPipeline: Pythonic DAGs                    │
│    • TapSpeak: Plain Python + CSV lexicon                   │
│    • BBTech Metrics: Simple CSV calculations                │
└─────────────────────────────────────────────────────────────┘
```

## Layer 1: Spatial / Network Core

### Scanpy + AnnData

**Purpose**: Core single-cell toolkit with efficient H5 backing for expression-level work

**Use Cases**:
- Preprocessing raw count matrices
- Clustering (Leiden, Louvain)
- Embeddings (UMAP, PHATE) that feed network maps
- Quality control and normalization

**Example**:
```python
from app.services.spatial_omics import SpatialOmicsService

service = SpatialOmicsService()

# Preprocess expression data
result = service.preprocess_expression_data(
    expression_matrix=expression_data,
    gene_names=genes,
    cell_names=cells
)

# Compute UMAP embeddings
embeddings = service.compute_embeddings(method="umap", n_neighbors=15)

# Perform clustering
clusters = service.perform_clustering(resolution=1.0, algorithm="leiden")
```

### Squidpy

**Purpose**: Thin spatial layer on top of Scanpy for tissue geometry

**Use Cases**:
- Build neighborhood graphs from spatial coordinates
- Extract image features at tissue locations
- Simple APIs for spatial analysis without custom image plumbing

**Example**:
```python
# Build spatial neighborhood graph
spatial_graph = service.build_spatial_neighborhood_graph(
    spatial_coords=tissue_coordinates,
    coord_type="generic",
    n_neighs=6
)

# Extract image features
features = service.extract_image_features(
    image_path="tissue_image.tif",
    spatial_coords=coordinates,
    features=["texture", "summary"]
)
```

### NetworkX

**Purpose**: Pure-Python graphs for prototype interactomes

**Use Cases**:
- Scale-free analysis
- Hub gravity calculations
- "Achilles heel" search
- Rapid prototyping of network algorithms

**Example**:
```python
from app.services.network import UniversalInteractomeService

network_service = UniversalInteractomeService()

# Validate scale-free topology
validation = network_service.validate_scale_free()

# Identify pan-cellular hubs
hubs = network_service.identify_pan_cellular_hubs()

# Simulate hub attack
attack_results = network_service.simulate_hub_attack(removal_fraction=0.2)
```

### Neo4j (Community)

**Purpose**: Persistent Network Cellular Map, queryable by clinicians and TapSpeak engine

**Use Cases**:
- Store universal interactome persistently
- Query disease modules by Cypher
- Provide graph visualization for frontend
- Enable multi-user access to network data

## Layer 2: Training / AI

### PyTorch

**Purpose**: Core deep learning aligned with GNN workflows

**Use Cases**:
- SpatialGCN implementations
- Causal scoring heads
- TapSpeak text embedders

**Integration**: Already integrated via PyTorch Geometric

### PyTorch Geometric (PyG)

**Purpose**: Focused GNN library with modular wheels

**Use Cases**:
- Message passing on interactomes and tissue graphs
- Built-in GNN layers (GCN, GAT, GraphSAGE)
- Graph data loaders for spatial omics

**Example**:
```python
# Export data for SpatialGCN
from app.services.spatial_omics import SpatialOmicsService

service = SpatialOmicsService()
gcn_data = service.export_for_spatialgcn()

# gcn_data contains:
# - expression_matrix
# - spatial_graph (adjacency)
# - embeddings
# - clusters
```

### scvi-tools

**Purpose**: Probabilistic models for single-cell data

**Use Cases**:
- Denoising expression data
- Batch correction across samples
- Latent spaces that feed causal/hub models
- Integration with AnnData objects

**Benefits**:
- Tight integration with AnnData/Scanpy
- Variational inference for robust embeddings
- Cell type discovery
- Compositional analysis

## Layer 3: Federated / Global Adoption

### FedLab (Simulation-Oriented)

**Purpose**: Python-native FL for experimenting with Overlay365 federation logic

**Use Cases**:
- Simulate 100s of "clinics/citizens" before deployment
- Test aggregation strategies
- Validate privacy mechanisms
- Prototype federated workflows

**Example**:
```python
from app.services.federated_learning import FederatedLearningService

fl_service = FederatedLearningService(mode="simulation")

# Simulate federation with 100 clients
simulation = fl_service.simulate_federation(
    n_clients=100,
    data_distribution="non_iid",
    client_type="clinic"
)

# Run training round
round_result = fl_service.federated_training_round(
    model_state={},
    client_data=client_datasets,
    aggregation_strategy="fedavg"
)
```

### OpenFL (Production)

**Purpose**: Production-grade FL from Linux Foundation

**Use Cases**:
- Real federated training across hospitals
- HIPAA-compliant deployments
- Secure aggregation protocols
- Framework-agnostic (works with PyTorch, TF)

**Example**:
```python
fl_service = FederatedLearningService(mode="production")

# Setup production federation
config = fl_service.setup_production_federation(
    collaborators=["hospital_A", "hospital_B", "hospital_C"],
    aggregator_address="https://aggregator.example.com",
    security_config={
        "tls_enabled": True,
        "client_auth": True,
        "differential_privacy": True
    }
)

# Configure privacy
privacy = fl_service.configure_privacy_preserving_training(
    differential_privacy=True,
    epsilon=1.0,
    secure_aggregation=True
)
```

### Overlay365 Network

**Purpose**: Hierarchical federation with citizens and clinics

**Example**:
```python
# Simulate Overlay365 network
overlay = fl_service.simulate_overlay365_network(
    n_citizens=365,
    n_clinics=100
)

# Results:
# - Citizens contribute edge data
# - Clinics aggregate local regions
# - Global model trained across all participants
# - Data stays local, only model updates shared
```

## Orchestration Without Bloat

### NetworkologyPipeline

**Purpose**: Pythonic pipeline framework lighter than Airflow/Nextflow

**Use Cases**:
- "ingest → map → analyze → intervene" DAGs
- Dependency resolution
- Error handling and retry logic
- Pipeline status monitoring

**Example**:
```python
from app.services.orchestration import NetworkologyPipeline

pipeline = NetworkologyPipeline("MyAnalysis")

# Add stages with dependencies
pipeline.add_stage("ingest", ingest_function, dependencies=[])
pipeline.add_stage("map", map_function, dependencies=["ingest"])
pipeline.add_stage("analyze", analyze_function, dependencies=["map"])
pipeline.add_stage("intervene", intervene_function, dependencies=["analyze"])

# Execute pipeline
results = pipeline.execute(initial_inputs={"gene": "TP53"})
```

### Pre-configured NetworkologyDAG

**Example**:
```python
from app.services.orchestration import NetworkologyDAG

# Use pre-configured 4-stage DAG
dag = NetworkologyDAG()
results = dag.run(gene="BRCA1")

# Automatically runs:
# 1. Ingest (OMIM + GenBank + KEGG)
# 2. Map (Build universal interactome)
# 3. Analyze (Causal discovery + hub identification)
# 4. Intervene (CRISPR design)
```

### TapSpeak Generator

**Purpose**: Plain Python + CSV lexicon for hook generation

**Use Cases**:
- Convert technical terms to plain language
- Generate patient-friendly explanations
- Update lexicon as needed
- No huge NLP stack required

**Example**:
```python
from app.services.orchestration import TapSpeakGenerator

tapspeak = TapSpeakGenerator()

# Generate plain-language hook
hook = tapspeak.generate_hook("Achilles_heel")
# Returns: "critical vulnerability"

# Update lexicon
tapspeak.update_lexicon(
    term="SpatialGCN",
    hook="tissue-aware AI",
    explanation="neural network that understands tissue geometry"
)

# Export to CSV
tapspeak.export_lexicon()
```

### BBTech Metrics

**Purpose**: Metric calculations using simple CSV stack

**Example**:
```python
from app.services.orchestration import BBTechMetrics

metrics = BBTechMetrics()

# Calculate Codex metrics
trueness = metrics.calculate_trueness(
    restored_edges=80,
    total_disrupted_edges=100
)  # 0.8

flow = metrics.calculate_flow(
    delivered_molecules=950,
    target_molecules=1000
)  # 0.95

gravity = metrics.calculate_gravity(
    hub_degree=50,
    hub_betweenness=0.35
)  # ~1.37

# Export to CSV
metrics.export_to_csv("/tmp/bbtech_metrics.csv")
```

## System Integration Flow

### Complete Workflow Example

```python
from app.services.spatial_omics import SpatialOmicsService
from app.services.network import UniversalInteractomeService
from app.services.federated_learning import FederatedLearningService
from app.services.orchestration import NetworkologyDAG

# 1. INGEST / MAP: Scanpy + Squidpy → AnnData + spatial graphs
spatial_service = SpatialOmicsService()

# Preprocess spatial omics data
spatial_service.preprocess_expression_data(
    expression_matrix=counts,
    gene_names=genes,
    cell_names=cells
)

# Build spatial neighborhood graph
spatial_graph = spatial_service.build_spatial_neighborhood_graph(
    spatial_coords=coordinates,
    n_neighs=6
)

# 2. MAP: NetworkX/Neo4j
network_service = UniversalInteractomeService()

# Integrate spatial and molecular networks
integrated_graph, metadata = spatial_service.integrate_with_network_map(
    spatial_graph=spatial_graph,
    gene_network=network_service.graph
)

# 3. ANALYZE: PyTorch + PyG + scvi-tools
# Export for SpatialGCN
gcn_data = spatial_service.export_for_spatialgcn()

# Train SpatialGCN with causal heads
# (Implementation depends on specific model architecture)

# 4. FEDERATE: FedLab/OpenFL
fl_service = FederatedLearningService(mode="simulation")

# Simulate federated training
simulation = fl_service.simulate_federation(n_clients=100)

# Wrap PyTorch model for federation
fed_model = fl_service.wrap_pytorch_model_for_federation(
    model_class="SpatialGCN",
    model_params={"hidden_channels": 64, "num_layers": 3}
)

# 5. EXPLAIN (TapSpeak)
from app.services.orchestration import TapSpeakGenerator

tapspeak = TapSpeakGenerator()
explanation = tapspeak.generate_hook("hub_gravity")

# 6. Or use pre-configured DAG for everything
dag = NetworkologyDAG()
complete_results = dag.run(gene="TP53")
```

## Dependencies Added

The following dependencies have been added to `requirements.txt`:

```python
# Spatial Omics & Single-Cell
scanpy==1.10.0           # Single-cell preprocessing and analysis
squidpy==1.4.1           # Spatial omics and tissue graphs
anndata==0.10.5          # Annotated data structures
scvi-tools==1.1.0        # Probabilistic single-cell models

# Federated Learning
fedlab==1.3.0            # Simulation-oriented federated learning
openfl==1.5              # Production federated learning

# Orchestration
ruffus==2.8.4            # Lightweight pipeline framework
```

## Benefits of This Architecture

### 1. **No Monoliths**
- Each layer is independent and composable
- Can use Scanpy without FedLab, or vice versa
- Easy to swap components (e.g., replace FedLab with Flower)

### 2. **Lean Stack**
- Total new dependencies: ~7 packages
- Each package is focused and lightweight
- No heavyweight platforms (Airflow, Kubeflow, etc.)

### 3. **Standard Tools**
- All packages are well-maintained and widely used
- Active communities and documentation
- Framework-agnostic (works with existing code)

### 4. **Production Ready**
- FedLab for development/testing
- OpenFL for production deployment
- Both support PyTorch models natively

### 5. **Easy Integration**
- Scanpy/Squidpy work seamlessly with PyTorch Geometric
- AnnData is the standard for single-cell data
- NetworkX graphs easily convert to PyG format

## Future Extensions

The composable architecture allows easy addition of:

1. **Alternative embedding methods** (PaCMAP, TriMAP)
2. **Additional FL frameworks** (Flower, PySyft)
3. **Advanced orchestration** (Prefect, Dagster)
4. **Enhanced NLP** (Small transformer models for TapSpeak)

All without breaking existing functionality or adding platform bloat.

## Performance Considerations

- **Scanpy**: Uses sparse matrices and H5 backing for memory efficiency
- **Squidpy**: Thin wrapper, minimal overhead
- **FedLab**: Python-native, good for simulation (100s of clients)
- **OpenFL**: Production-optimized, handles real deployments
- **NetworkologyPipeline**: Pure Python, no database required

## Security & Privacy

### Federated Learning Privacy

```python
# Configure differential privacy
fl_service.configure_privacy_preserving_training(
    differential_privacy=True,
    epsilon=1.0,        # Privacy budget
    delta=1e-5,         # Privacy parameter
    secure_aggregation=True
)

# GDPR compliant, HIPAA compatible
# Data stays local, only model updates shared
```

## Testing the Toolchain

See `backend/tests/` for validation tests covering:
- Spatial omics preprocessing
- Neighborhood graph construction
- Federated learning simulation
- Pipeline orchestration
- TapSpeak generation

## Documentation

- **This file (TOOLCHAIN.md)**: Architecture overview
- **API.md**: API endpoint documentation
- **QUICKSTART.md**: Getting started guide
- **ARCHITECTURE.md**: Full system architecture

## Support

For toolchain-specific questions:
- Scanpy: https://scanpy.readthedocs.io/
- Squidpy: https://squidpy.readthedocs.io/
- FedLab: https://fedlab.readthedocs.io/
- OpenFL: https://openfl.readthedocs.io/
