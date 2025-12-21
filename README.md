# NetworkCellularMap v2.0

**Networkology Core Engine - Organ Agnostic Network Diagnosis**

## Overview

NetworkCellularMap v2.0 is a revolutionary bioinformatics platform that implements organ-agnostic network diagnosis. Instead of treating organ-specific symptoms, it targets the underlying network dysfunction at the cellular level.

### Core Principle

> Single mutation propagates across all cells; target network dysfunction, not organ symptoms.

## Architecture

### Tech Stack

#### Backend
- **FastAPI**: High-performance Python web framework
- **Neo4j 5.20**: Graph database for network storage
- **NetworkX 3.3**: Graph analysis and algorithms
- **PyTorch Geometric**: Graph neural networks

#### Frontend
- **Next.js 15**: React framework for server-side rendering
- **Cytoscape.js 3.24**: Network visualization
- **Three.js**: 3D visualizations

#### AI/ML
- **CausalNex**: Causal discovery algorithms
- **DoWhy**: Causal inference
- **PyG 2.5**: Graph machine learning
- **scikit-learn**: Traditional ML algorithms

#### Bioinformatics
- **Biopython 1.83**: Biological sequence analysis
- **KEGGREST**: KEGG pathway integration
- **OMIM API**: Genetic disorder database
- **Entrez**: NCBI database access

#### Composable Toolchain
**Layer 1: Spatial/Network Core**
- **Scanpy 1.10**: Single-cell preprocessing and analysis
- **Squidpy 1.4**: Spatial omics and tissue graphs
- **AnnData 0.10**: Annotated data structures with H5 backing

**Layer 2: Training/AI**
- **scvi-tools 1.1**: Probabilistic single-cell models

**Layer 3: Federated Learning**
- **FedLab 1.3**: Simulation-oriented federated learning
- **OpenFL 1.5**: Production federated learning

**Orchestration**
- **Ruffus 2.8**: Lightweight pipeline framework
- See [TOOLCHAIN.md](docs/TOOLCHAIN.md) for complete architecture

## Global Schemas

### CellAgnosticNode
Universal node present in all cell types:
```python
{
  "universal_id": "string",
  "genome_position": {"chr": "string", "pos": "int", "ref": "string", "alt": "string"},
  "present_in_all_cells": true,
  "network_role": "enum['hub', 'connector', 'leaf', 'regulator']"
}
```

### PanCellularEdge
Universal relationship across all cells:
```python
{
  "relation_type": "enum['PPI', 'REGULATES', 'METABOLIC', 'VIRAL_HOST']",
  "exists_in_all_cells": true,
  "disruption_impact": "float[-1,1]"
}
```

## Modules

### 1. Data Ingestion
**Anti-Reductionist Federation** - Integrates multiple biological databases:
- OMIM: Pan-cellular phenotype data
- GenBank: Universal sequence data
- KEGG: Cell-agnostic pathways

BioKleisli queries join data across sources based on universal genomic positions.

### 2. Network Mapping
**Universal Interactome** - Constructs pan-cellular network:
- Scale-free validation (power law α: 2.1-2.7)
- Hub identification (top 5% by degree centrality)
- Topology analysis

### 3. AI Analysis
**AI Scientist** - Causal discovery and vulnerability analysis:
- PC-stable algorithm for causal discovery
- NOTEARS for acyclic graph generation
- Achilles heel protocol for hub vulnerability

### 4. Codex Overlay
**Networkologist Metrics**:
- **Trueness**: Pan-cellular restoration score
- **Flow**: Universal delivery efficiency
- **Gravity**: Universal hub impact score

**Gamification Layer**:
- Quests: Fix universal hubs, collapse disease modules
- Achievements: Networkologist levels, circuit mastery

### 5. Network Repair
**Universal CRISPR-Cas9**:
- One sgRNA fixes all cell instances
- HDR template with wildtype sequence
- AAV9 multitropic delivery (crosses BBB + muscle + liver)

## API Endpoints

### POST /api/v1/networkologist/diagnose
Diagnose patient with organ-agnostic analysis
```json
{
  "patient_genome": {"mutation_id": {"chr": "17", "pos": 7577548, "ref": "C", "alt": "T"}},
  "symptoms_multi_organ": ["fatigue", "cognitive_decline", "muscle_weakness"]
}
```

### GET /api/v1/universal_hub/{mutation_id}
Pan-cellular impact analysis for specific mutation

### POST /api/v1/repair_design/{hub_id}
Design CRISPR repair strategy with bill of materials

## Installation

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/ncsound919/Cellular-Map.git
cd Cellular-Map

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Neo4j Browser: http://localhost:7474
```

### Manual Installation

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes/deployment.yaml

# Check deployment status
kubectl get pods -n networkology

# Access services
kubectl port-forward -n networkology svc/frontend 3000:80
```

## Usage Examples

### 1. Diagnose a Patient

```python
import requests

diagnosis = requests.post('http://localhost:8000/api/v1/networkologist/diagnose', json={
    "patient_genome": {
        "TP53_mutation": {"chr": "17", "pos": 7577548, "ref": "C", "alt": "T"}
    },
    "symptoms_multi_organ": ["fatigue", "weight_loss"],
    "patient_id": "PAT001"
})

print(diagnosis.json())
```

### 2. Analyze Universal Hub

```python
hub_analysis = requests.get('http://localhost:8000/api/v1/universal_hub/TP53')
print(hub_analysis.json())
```

### 3. Design CRISPR Repair

```python
repair = requests.post('http://localhost:8000/api/v1/repair_design/TP53', json={
    "hub_id": "TP53",
    "mutation_ids": ["TP53_R273H"],
    "target_tissues": ["heart", "brain", "liver"]
})

print(repair.json())
```

## Dashboard Views

### Universal Mutation Map
3D force-directed graph showing mutations across different tissues with Codex metrics overlay.

### Pan-Cellular Hub Radar
Multi-dimensional impact visualization across organs (heart, brain, liver, muscle).

### Disease Module Collapse
Before/after network diffusion showing intervention effects.

## Network Analysis

### Scale-Free Validation
- Power law fitting: α ∈ [2.1, 2.7]
- Kolmogorov-Smirnov test: p < 0.05

### Hub Vulnerability
- Random failure: 99% robust
- Hub attack: Network collapses at 20% removal

## CRISPR Design Parameters

### Universal gRNA
- Length: 20 nucleotides
- Cell-type agnostic
- Off-target filtered

### AAV9 Vector
- Capacity: 4.7 kb
- Titer: >1e13 vg/ml
- Pan-tissue biodistribution: 90%+

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend linting
cd backend
flake8 app/
black app/

# Frontend linting
cd frontend
npm run lint
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

See LICENSE file for details.

## Citation

If you use NetworkCellularMap in your research, please cite:

```
NetworkCellularMap v2.0: Organ-Agnostic Network Diagnosis Platform
https://github.com/ncsound919/Cellular-Map
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/ncsound919/Cellular-Map/issues
- Documentation: See `/docs` directory

## Acknowledgments

Built on principles of systems biology, network medicine, and precision therapeutics. 
