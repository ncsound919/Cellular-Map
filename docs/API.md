# API Architecture

## Overview

The NetworkCellularMap API follows RESTful principles and provides three main endpoint groups:

## Endpoint Groups

### 1. Networkologist Diagnosis (`/api/v1/networkologist`)

#### POST /diagnose
Performs comprehensive organ-agnostic network diagnosis.

**Request:**
```json
{
  "patient_genome": {
    "mutation_1": {
      "chr": "17",
      "pos": 7577548,
      "ref": "C",
      "alt": "T"
    }
  },
  "symptoms_multi_organ": ["fatigue", "cognitive_decline"],
  "patient_id": "PAT001"
}
```

**Response:**
```json
{
  "patient_id": "PAT001",
  "network_dysfunction": [
    {
      "module_id": "MODULE_0",
      "affected_tissues": ["heart", "brain"],
      "hub_nodes": ["TP53", "BRCA1"],
      "dysfunction_score": 0.85,
      "causal_mutations": ["mutation_1"]
    }
  ],
  "universal_targets": [
    {
      "hub_id": "TP53",
      "universal_degree_centrality": 0.92,
      "betweenness_centrality": 0.87,
      "eigenvector_centrality": 0.91,
      "tissues": ["heart", "brain", "liver"],
      "gravity_score": 0.89
    }
  ],
  "codex_scores": {
    "trueness": 0.85,
    "flow": 0.90,
    "gravity": 0.88
  },
  "recommended_interventions": [...]
}
```

### 2. Universal Hub Analysis (`/api/v1/universal_hub`)

#### GET /{mutation_id}
Analyzes pan-cellular impact of a specific mutation.

**Response:**
```json
{
  "mutation_id": "TP53",
  "pan_cellular_impact": {
    "gravity_score": 0.89,
    "affected_module_size": 145,
    "module_nodes": ["BRCA1", "EGFR", ...],
    "network_criticality": "high"
  },
  "topology_analysis": {...},
  "tissues_affected": ["heart", "brain", "liver", "muscle"],
  "universal": true
}
```

#### GET /{mutation_id}/neighbors
Gets neighboring nodes in the network.

### 3. Repair Design (`/api/v1/repair_design`)

#### POST /{hub_id}
Designs CRISPR repair strategy.

**Request:**
```json
{
  "hub_id": "TP53",
  "mutation_ids": ["TP53_R273H"],
  "target_tissues": ["heart", "brain", "liver"]
}
```

**Response:**
```json
{
  "hub_id": "TP53",
  "crispr_payload": {
    "target_id": "TP53",
    "grna_sequence": "ATCGATCGATCGATCGATCG",
    "hdr_template": "HDR_TEMPLATE_1020bp",
    "delivery_vector": "AAV9_multitropic",
    "predicted_efficiency": 0.89
  },
  "aav9_vector": {
    "serotype": "AAV9",
    "capacity_kb": 4.7,
    "payload_size_kb": 4.5,
    "fits_capacity": true,
    "titer_vg_ml": 1.5e13,
    "biodistribution": {...}
  },
  "validation_results": {...},
  "estimated_success_rate": 0.92
}
```

## Error Handling

All endpoints return standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

Error responses follow this format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider adding rate limiting middleware.

## Authentication

Currently no authentication is required. For production deployment, implement OAuth2 or JWT authentication.
