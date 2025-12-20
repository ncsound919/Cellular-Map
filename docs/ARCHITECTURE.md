# NetworkCellularMap v2.0 Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     NetworkCellularMap v2.0                      │
│            Organ-Agnostic Network Diagnosis Platform             │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐
│   External APIs   │         │      Users       │
│  ┌────────────┐  │         │  ┌────────────┐  │
│  │   OMIM     │  │         │  │ Researchers │  │
│  │  GenBank   │  │         │  │ Clinicians  │  │
│  │   KEGG     │  │         │  │  Patients   │  │
│  └────────────┘  │         │  └────────────┘  │
└────────┬─────────┘         └────────┬─────────┘
         │                            │
         ▼                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Next.js 15 Application                  │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │ Universal    │  │ Pan-Cellular │  │    Codex     │   │  │
│  │  │ Mutation Map │  │  Hub Radar   │  │   Metrics    │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │  (Cytoscape.js)    (Canvas Radar)    (Progress Bars)    │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────┬─────────────────────────────────────────────────────────┘
         │
         │ HTTP/REST API
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Backend Layer                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Application                     │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │Networkologist│  │Universal Hub │  │Repair Design │   │  │
│  │  │   Diagnose   │  │   Analysis   │  │   Service    │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     Service Layer                          │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │  │
│  │  │ Ingestion   │ │  Network    │ │AI Scientist │        │  │
│  │  │  Service    │ │  Mapping    │ │  Service    │        │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘        │  │
│  │  ┌─────────────┐ ┌─────────────┐                        │  │
│  │  │   Codex     │ │   Repair    │                        │  │
│  │  │  Metrics    │ │   Engine    │                        │  │
│  │  └─────────────┘ └─────────────┘                        │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────┬────────────────────────────────────────────────┬────────┘
         │                                                │
         ▼                                                ▼
┌─────────────────────┐                      ┌─────────────────────┐
│  Data Storage Layer │                      │    Cache Layer      │
│  ┌───────────────┐  │                      │  ┌───────────────┐  │
│  │   Neo4j 5.20  │  │                      │  │     Redis     │  │
│  │  Graph Store  │  │                      │  │  Key-Value DB │  │
│  │               │  │                      │  │               │  │
│  │ • Nodes       │  │                      │  │ • Sessions    │  │
│  │ • Edges       │  │                      │  │ • Results     │  │
│  │ • Indexes     │  │                      │  │ • Cache       │  │
│  └───────────────┘  │                      │  └───────────────┘  │
└─────────────────────┘                      └─────────────────────┘
```

## Data Flow

### 1. Diagnosis Pipeline

```
User Request
    │
    ▼
┌─────────────────────────────────────┐
│  Patient Genome + Symptoms          │
│  {                                  │
│    "genome": {...},                 │
│    "symptoms": ["fatigue", ...]     │
│  }                                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Data Ingestion Service             │
│  • BioKleisli Queries               │
│  • OMIM/GenBank/KEGG Integration    │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Network Mapping Service            │
│  • Universal Interactome Builder    │
│  • Scale-Free Validation            │
│  • Hub Identification               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  AI Scientist Service               │
│  • Causal Discovery (PC-stable)     │
│  • Network Vulnerability Analysis   │
│  • Disease Module Detection         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Codex Metrics Service              │
│  • Trueness Calculation             │
│  • Flow Assessment                  │
│  • Gravity Scoring                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Diagnosis Response                 │
│  {                                  │
│    "network_dysfunction": [...],    │
│    "universal_targets": [...],      │
│    "codex_scores": {...},           │
│    "interventions": [...]           │
│  }                                  │
└─────────────────────────────────────┘
```

### 2. Repair Design Pipeline

```
Hub ID + Mutation IDs
    │
    ▼
┌─────────────────────────────────────┐
│  Target Selection                   │
│  • Pan-Cellular Hubs                │
│  • High Gravity Nodes               │
│  • Causal Drivers                   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  CRISPR Design Service              │
│  • Universal gRNA Design            │
│  • HDR Template Generation          │
│  • Efficiency Prediction            │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Viral Vector Service               │
│  • AAV9 Multitropic Design          │
│  • Biodistribution Analysis         │
│  • Capacity Validation              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Network Repair Simulation          │
│  • Gillespie Algorithm              │
│  • Success Prediction               │
│  • Validation Results               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Repair Design Response             │
│  {                                  │
│    "crispr_payload": {...},         │
│    "aav9_vector": {...},            │
│    "validation": {...},             │
│    "success_rate": 0.92             │
│  }                                  │
└─────────────────────────────────────┘
```

## Module Architecture

### Backend Modules

```
backend/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── endpoints/
│   │   │   ├── networkologist.py    # Diagnosis endpoint
│   │   │   ├── universal_hub.py     # Hub analysis endpoint
│   │   │   └── repair_design.py     # Repair design endpoint
│   │   └── router.py                # Main API router
│   │
│   ├── core/                   # Core configuration
│   │   └── config.py                # Settings and environment
│   │
│   ├── db/                     # Database layer
│   │   └── neo4j.py                 # Neo4j connection and queries
│   │
│   ├── models/                 # Data models
│   │   └── schemas.py               # Pydantic schemas
│   │
│   └── services/               # Business logic
│       ├── ingestion.py             # Data ingestion (OMIM/GenBank/KEGG)
│       ├── network.py               # Network mapping (NetworkX)
│       ├── ai_scientist.py          # Causal discovery & vulnerability
│       ├── codex.py                 # Codex metrics & gamification
│       └── repair.py                # CRISPR design & repair engine
│
└── main.py                     # FastAPI application entry point
```

### Frontend Modules

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page
│   └── globals.css             # Global styles
│
└── components/
    └── dashboard/
        ├── NetworkologistDashboard.tsx   # Main dashboard
        ├── UniversalMutationMap.tsx      # Network visualization
        ├── PanCellularHubRadar.tsx       # Radar chart
        └── CodexMetrics.tsx              # Metrics display
```

## Technology Stack Mapping

```
┌─────────────────────────────────────────────────────────────┐
│                     Technology Layers                        │
├─────────────────────────────────────────────────────────────┤
│ Presentation  │ Next.js 15, React 18, TypeScript            │
│               │ Cytoscape.js 3.24, Three.js                 │
├─────────────────────────────────────────────────────────────┤
│ API Gateway   │ FastAPI, Uvicorn                            │
├─────────────────────────────────────────────────────────────┤
│ Business      │ NetworkX 3.3 (Graph Analysis)               │
│ Logic         │ CausalNex (Causal Discovery)                │
│               │ DoWhy (Causal Inference)                    │
│               │ PyTorch Geometric 2.5 (Graph ML)            │
│               │ scikit-learn (Traditional ML)               │
│               │ Biopython 1.83 (Bioinformatics)             │
├─────────────────────────────────────────────────────────────┤
│ Data Access   │ Neo4j Python Driver 5.20                    │
│               │ Redis Python Client                         │
├─────────────────────────────────────────────────────────────┤
│ Storage       │ Neo4j 5.20 (Graph Database)                 │
│               │ Redis 7 (Cache)                             │
├─────────────────────────────────────────────────────────────┤
│ External APIs │ OMIM API, NCBI Entrez, KEGG REST            │
├─────────────────────────────────────────────────────────────┤
│ Container     │ Docker, Docker Compose                      │
├─────────────────────────────────────────────────────────────┤
│ Orchestration │ Kubernetes, Horizontal Pod Autoscaler       │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Namespace: networkology                │    │
│  │                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │    │
│  │  │   Frontend   │  │   Backend    │  │  Redis   │ │    │
│  │  │  Deployment  │  │  Deployment  │  │   Pod    │ │    │
│  │  │  (2 replicas)│  │  (3 replicas)│  │          │ │    │
│  │  │              │  │    + HPA     │  │          │ │    │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │    │
│  │                                                      │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │         Neo4j StatefulSet (3 replicas)       │  │    │
│  │  │         + PersistentVolumeClaims             │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  │                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │  Frontend    │  │  AI-Scientist│               │    │
│  │  │   Service    │  │   Service    │               │    │
│  │  │ LoadBalancer │  │  ClusterIP   │               │    │
│  │  └──────────────┘  └──────────────┘               │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
         │                        │
         │                        │
         ▼                        ▼
    Internet Users          Internal Services
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│         Security Layers                  │
├─────────────────────────────────────────┤
│ 1. HTTPS/TLS                            │
│    └─ Encrypted communication           │
├─────────────────────────────────────────┤
│ 2. Authentication (Future)              │
│    └─ OAuth2/JWT tokens                 │
├─────────────────────────────────────────┤
│ 3. Authorization (Future)               │
│    └─ Role-based access control         │
├─────────────────────────────────────────┤
│ 4. API Rate Limiting (Future)           │
│    └─ Prevent abuse                     │
├─────────────────────────────────────────┤
│ 5. Input Validation                     │
│    └─ Pydantic schemas                  │
├─────────────────────────────────────────┤
│ 6. Database Security                    │
│    └─ Neo4j authentication              │
├─────────────────────────────────────────┤
│ 7. Network Policies (K8s)               │
│    └─ Pod-to-pod traffic control        │
└─────────────────────────────────────────┘
```

## Scalability Strategy

1. **Horizontal Scaling**: Backend pods auto-scale based on CPU/memory
2. **Database Clustering**: Neo4j runs in cluster mode (3 replicas)
3. **Caching**: Redis reduces database load
4. **Load Balancing**: Kubernetes services distribute traffic
5. **Stateless Services**: Backend is stateless for easy scaling
6. **CDN (Future)**: Frontend static assets via CDN
