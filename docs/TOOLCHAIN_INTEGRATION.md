# Composable Toolchain Integration Guide

This guide shows how to integrate the new composable toolchain components into your NetworkCellularMap workflows.

## Quick Start

### Installation

The composable toolchain dependencies are included in `backend/requirements.txt`:

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- Scanpy + AnnData (spatial omics)
- Squidpy (tissue graphs)
- scvi-tools (probabilistic models)
- FedLab (FL simulation)
- OpenFL (FL production)
- Ruffus (orchestration)

### Basic Usage

#### 1. Spatial Omics Analysis

```python
from app.services.spatial_omics import SpatialOmicsService

# Initialize service
spatial = SpatialOmicsService()

# Preprocess single-cell data
result = spatial.preprocess_expression_data(
    expression_matrix=counts,
    gene_names=genes,
    cell_names=cells
)

# Compute UMAP embeddings
embeddings = spatial.compute_embeddings(method="umap")

# Build spatial neighborhood graph
spatial_graph = spatial.build_spatial_neighborhood_graph(
    spatial_coords=coordinates,
    n_neighs=6
)
```

#### 2. Federated Learning

```python
from app.services.federated_learning import FederatedLearningService

# Simulation mode (for testing)
fl_service = FederatedLearningService(mode="simulation")

# Simulate 100 clinics
simulation = fl_service.simulate_federation(
    n_clients=100,
    client_type="clinic"
)

# Configure privacy
privacy = fl_service.configure_privacy_preserving_training(
    differential_privacy=True,
    epsilon=1.0
)
```

#### 3. Pipeline Orchestration

```python
from app.services.orchestration import NetworkologyDAG

# Run complete workflow
dag = NetworkologyDAG()
results = dag.run(gene="TP53")

# Results include: ingest → map → analyze → intervene
```

## Integration Patterns

### Pattern 1: Spatial + Network Analysis

Combine spatial tissue graphs with molecular networks:

```python
from app.services.spatial_omics import SpatialOmicsService
from app.services.network import UniversalInteractomeService

# Build both graphs
spatial_service = SpatialOmicsService()
network_service = UniversalInteractomeService()

# Build spatial graph from tissue
spatial_graph = spatial_service.build_spatial_neighborhood_graph(
    spatial_coords=tissue_coordinates,
    n_neighs=6
)

# Integrate with molecular network
integrated, metadata = spatial_service.integrate_with_network_map(
    spatial_graph=spatial_graph,
    gene_network=network_service.graph
)

print(f"Integrated: {metadata['total_nodes']} nodes")
```

### Pattern 2: Federated GNN Training

Train graph neural networks across multiple sites:

```python
from app.services.spatial_omics import SpatialOmicsService
from app.services.federated_learning import FederatedLearningService

# Prepare data for GNN
spatial = SpatialOmicsService()
# ... preprocess data ...
gcn_data = spatial.export_for_spatialgcn()

# Setup federated learning
fl = FederatedLearningService(mode="production")

# Wrap PyTorch model
fed_model = fl.wrap_pytorch_model_for_federation(
    model_class="SpatialGCN",
    model_params={"hidden_channels": 64}
)

# Configure for HIPAA compliance
privacy = fl.configure_privacy_preserving_training(
    differential_privacy=True,
    epsilon=1.0,
    secure_aggregation=True
)
```

### Pattern 3: Complete Pipeline with TapSpeak

Run analysis and generate plain-language explanations:

```python
from app.services.orchestration import NetworkologyDAG, TapSpeakGenerator

# Run full analysis
dag = NetworkologyDAG()
results = dag.run(gene="BRCA1")

# Generate explanations
tapspeak = TapSpeakGenerator()

# Convert technical terms to hooks
hub_hook = tapspeak.generate_hook("hub")
# Returns: "network traffic controller"

achilles_hook = tapspeak.generate_hook("Achilles_heel")
# Returns: "critical vulnerability"
```

## API Integration

### REST API Endpoints (Planned)

While the services are implemented, API endpoints can be added as needed:

```python
# Example endpoint (to be added to backend/app/api/endpoints/)

from fastapi import APIRouter
from app.services.spatial_omics import SpatialOmicsService

router = APIRouter()

@router.post("/spatial/preprocess")
async def preprocess_spatial_data(
    expression_data: dict,
    gene_names: list,
    cell_names: list
):
    service = SpatialOmicsService()
    result = service.preprocess_expression_data(
        expression_matrix=expression_data,
        gene_names=gene_names,
        cell_names=cell_names
    )
    return result

@router.post("/federated/simulate")
async def simulate_federation(n_clients: int = 100):
    service = FederatedLearningService(mode="simulation")
    result = service.simulate_federation(n_clients=n_clients)
    return result
```

## Data Flow

### Typical Workflow

```
1. INGEST
   └─> Scanpy: Load and QC single-cell data
       └─> AnnData object created

2. PREPROCESS
   └─> Scanpy: Normalize, scale, HVG selection
       └─> Squidpy: Build spatial neighborhood graph

3. EMBED
   └─> Scanpy: UMAP/PHATE embedding
       └─> scvi-tools: Probabilistic latent space (optional)

4. ANALYZE
   └─> NetworkX: Network topology analysis
       └─> PyTorch Geometric: SpatialGCN training
       └─> Export predictions

5. FEDERATE (if multi-site)
   └─> FedLab: Simulate federation
       └─> OpenFL: Deploy to hospitals
       └─> Aggregate models with privacy

6. EXPLAIN
   └─> TapSpeak: Generate hooks
       └─> BBTech: Calculate metrics
```

## Performance Tips

### Memory Optimization

Scanpy uses efficient sparse matrices and H5 backing:

```python
# For large datasets, use backed mode
import scanpy as sc

adata = sc.read_h5ad('data.h5ad', backed='r')
# Only loads metadata, not full matrix
```

### Parallel Processing

NetworkX can use parallel backends:

```python
import networkx as nx

# Some algorithms support n_jobs parameter
# Use -1 for all cores
```

### Federated Learning Efficiency

```python
# Use gradient compression to reduce communication
fl_service = FederatedLearningService(mode="production")

# Compress updates (configured in privacy settings)
privacy = fl_service.configure_privacy_preserving_training(
    differential_privacy=True,
    epsilon=1.0,
    secure_aggregation=True  # Includes compression
)
```

## Testing

### Unit Tests

```bash
cd backend
python tests/test_toolchain.py
```

### Integration Test

```bash
cd backend
python examples/toolchain_usage.py
```

### Expected Output

```
=== Spatial Omics Example ===
✓ Preprocessed 1000 cells, 2000 genes
✓ Found 2000 highly variable genes
✓ Embedding shape: (1000, 2)
✓ Found 5 clusters
✓ Spatial graph: 1000 nodes, 6000 edges

=== Federated Learning Example ===
✓ Simulated 100 clients
✓ Total samples: 45000
✓ Framework: FedLab

=== Orchestration Example ===
✓ Pipeline: NetworkologyCore
✓ Status: completed
✓ Execution order: ingest → map → analyze → intervene
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`:

```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

### Scanpy/Squidpy Issues

These packages require scientific Python stack:

```bash
# Install with all dependencies
pip install scanpy[leiden] squidpy
```

### FedLab/OpenFL Issues

For simulation only:

```bash
pip install fedlab
```

For production deployment:

```bash
pip install openfl
# Follow OpenFL setup guide for workspace configuration
```

## Migration Guide

### From Existing Code

If you have existing single-cell analysis code:

**Before:**
```python
# Custom preprocessing
data = normalize(raw_counts)
data = scale(data)
```

**After:**
```python
from app.services.spatial_omics import SpatialOmicsService

spatial = SpatialOmicsService()
result = spatial.preprocess_expression_data(
    expression_matrix=raw_counts,
    gene_names=genes,
    cell_names=cells
)
# Handles normalization, scaling, HVG selection
```

### From Centralized to Federated

**Before:**
```python
# Centralized training
model.fit(all_data)
```

**After:**
```python
from app.services.federated_learning import FederatedLearningService

fl = FederatedLearningService(mode="production")

# Data stays at each site
# Only model updates are shared
config = fl.setup_production_federation(
    collaborators=["Hospital_A", "Hospital_B"],
    aggregator_address="https://agg.example.com"
)
```

## Best Practices

### 1. Use AnnData for Single-Cell

Always store single-cell data in AnnData format:

```python
import anndata

adata = anndata.AnnData(
    X=counts,  # expression matrix
    obs=cell_metadata,  # cell annotations
    var=gene_metadata   # gene annotations
)

# Save for later
adata.write_h5ad('data.h5ad')
```

### 2. Privacy-First Federated Learning

Always configure privacy when deploying:

```python
# HIPAA-compliant configuration
privacy = fl.configure_privacy_preserving_training(
    differential_privacy=True,
    epsilon=1.0,  # Strict privacy
    delta=1e-6,
    secure_aggregation=True
)
```

### 3. Pipeline Over Scripts

Use pipelines for reproducibility:

```python
from app.services.orchestration import NetworkologyPipeline

pipeline = NetworkologyPipeline("MyAnalysis")
pipeline.add_stage("ingest", ingest_func)
pipeline.add_stage("analyze", analyze_func, dependencies=["ingest"])

# Save and version pipeline
pipeline.execute(initial_inputs={"gene": "TP53"})
```

## Additional Resources

- **Scanpy Documentation**: https://scanpy.readthedocs.io/
- **Squidpy Documentation**: https://squidpy.readthedocs.io/
- **FedLab Documentation**: https://fedlab.readthedocs.io/
- **OpenFL Documentation**: https://openfl.readthedocs.io/
- **TOOLCHAIN.md**: Complete architecture reference
- **examples/toolchain_usage.py**: Full working examples

## Support

For toolchain integration questions:
- Check examples in `backend/examples/toolchain_usage.py`
- Review tests in `backend/tests/test_toolchain.py`
- See complete architecture in `docs/TOOLCHAIN.md`
- GitHub Issues: https://github.com/ncsound919/Cellular-Map/issues
