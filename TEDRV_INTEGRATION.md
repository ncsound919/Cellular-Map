# TED-RV Integration Guide

## Overview

This guide provides detailed instructions for integrating the TED-RV (Therapeutic Epitope Design & Real-Time Validation) platform into your TumorTrack Institutional deployment.

## Prerequisites

### Infrastructure Requirements

#### Computational Resources

**Minimum (Development/Testing):**
- 16GB RAM
- 4-core CPU
- 100GB disk space
- Internet connectivity for cloud APIs

**Recommended (Production):**
- 64GB RAM
- 16-core CPU
- 1TB NVMe SSD
- GPU (NVIDIA A100 40GB) for local AlphaFold 3
- 10 Gbps network connection

#### Lab Equipment (Full Deployment)

**Required for Clinical Operations:**
1. **CRISPR 3.0 Benchtop Workstation** (~$200,000)
   - AI-designed enzyme library
   - Real-time feedback sensors
   - Automated electroporation system
   - Cell viability monitoring

2. **RAEFISH Imaging System** (~$300,000)
   - Single-molecule resolution microscope
   - Spatial transcriptomics software
   - High-throughput imaging stage
   - GPU workstation for image processing

3. **Patient-Derived Organoid (PDO) Culture System** (~$50,000)
   - 3D culture incubators
   - Organoid imaging system
   - Automated media handling

4. **Biosafety Infrastructure**
   - BSL-2 certified lab space (200 sq ft minimum)
   - Class II biosafety cabinets
   - Liquid nitrogen storage for cells
   - Waste disposal system

### Software Requirements

- PostgreSQL 15+ with `tedrv` schema
- Redis 7+ for workflow state caching
- Python 3.11+
- Docker 24+ (for containerized services)
- Kubernetes 1.27+ (for production orchestration)

### API Access

**Required External Services:**
- AlphaFold 3 API (cloud or self-hosted)
- Protein LLM API (e.g., ESM-2, ProtGPT)

**Optional Services:**
- CRISPR design APIs (e.g., Benchling, Synthego)
- Genomic data repositories (dbSNP, gnomAD)

---

## Installation Steps

### 1. Database Setup

#### Create TED-RV Schema

```sql
-- Connect to your TumorTrack database
psql -U tumortrack -d tumortrack_db

-- Create tedrv schema
CREATE SCHEMA IF NOT EXISTS tedrv;

-- Grant permissions
GRANT USAGE ON SCHEMA tedrv TO tumortrack_app;
GRANT ALL ON SCHEMA tedrv TO tumortrack_admin;

-- Run migration script
\i /path/to/migrations/tedrv_schema.sql
```

#### Database Migration Script

Create `migrations/tedrv_schema.sql`:

```sql
-- TED-RV Database Schema Migration
-- Version: 1.0.0

SET search_path TO tedrv;

-- Genomic Profiles
CREATE TABLE genomic_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL,
    institution_id UUID NOT NULL,
    hla_alleles TEXT[] NOT NULL,
    tumor_mutations JSONB NOT NULL,
    tumor_wes_path TEXT,  -- Encrypted S3 path
    normal_wes_path TEXT,  -- Encrypted S3 path
    tumor_burden_mb FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_patient FOREIGN KEY (patient_id) 
        REFERENCES core.patients(patient_id) ON DELETE CASCADE,
    CONSTRAINT fk_institution FOREIGN KEY (institution_id) 
        REFERENCES core.institutions(institution_id) ON DELETE CASCADE
);

CREATE INDEX idx_genomic_profiles_patient ON genomic_profiles(patient_id);
CREATE INDEX idx_genomic_profiles_institution ON genomic_profiles(institution_id);

-- Neoepitope Predictions
CREATE TABLE neoepitope_predictions (
    epitope_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES genomic_profiles(profile_id) ON DELETE CASCADE,
    peptide_sequence VARCHAR(11) NOT NULL,
    source_mutation TEXT NOT NULL,
    hla_allele VARCHAR(50) NOT NULL,
    binding_affinity_nm FLOAT NOT NULL,
    alphafold3_confidence FLOAT NOT NULL CHECK (alphafold3_confidence BETWEEN 0 AND 1),
    immunogenicity_score FLOAT NOT NULL CHECK (immunogenicity_score BETWEEN 0 AND 1),
    cross_reactivity_risk FLOAT NOT NULL CHECK (cross_reactivity_risk BETWEEN 0 AND 1),
    rank INT NOT NULL CHECK (rank BETWEEN 1 AND 10),
    structure_pdb_path TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_neoepitopes_profile ON neoepitope_predictions(profile_id);
CREATE INDEX idx_neoepitopes_rank ON neoepitope_predictions(rank);
CREATE INDEX idx_neoepitopes_affinity ON neoepitope_predictions(binding_affinity_nm);

-- TCR Designs
CREATE TABLE tcr_designs (
    tcr_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    epitope_id UUID NOT NULL REFERENCES neoepitope_predictions(epitope_id) ON DELETE CASCADE,
    alpha_chain_sequence TEXT NOT NULL,
    beta_chain_sequence TEXT NOT NULL,
    predicted_affinity FLOAT NOT NULL,
    off_target_score FLOAT NOT NULL,
    design_method VARCHAR(100) DEFAULT 'alphafold3_optimization',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tcr_designs_epitope ON tcr_designs(epitope_id);

-- CRISPR Edits
CREATE TABLE crispr_edits (
    edit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tcr_id UUID NOT NULL REFERENCES tcr_designs(tcr_id) ON DELETE CASCADE,
    target_genes TEXT[] NOT NULL,
    guide_rnas TEXT[] NOT NULL,
    on_target_efficiency FLOAT NOT NULL CHECK (on_target_efficiency >= 0 AND on_target_efficiency <= 1),
    off_target_rate FLOAT NOT NULL CHECK (off_target_rate >= 0 AND off_target_rate <= 1),
    adaptive_feedback JSONB,
    cell_viability FLOAT DEFAULT 0.998,
    editing_time_hours FLOAT DEFAULT 24.0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_crispr_edits_tcr ON crispr_edits(tcr_id);
CREATE INDEX idx_crispr_edits_efficiency ON crispr_edits(on_target_efficiency);

-- Spatial Validations
CREATE TABLE spatial_validations (
    validation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    edit_id UUID NOT NULL REFERENCES crispr_edits(edit_id) ON DELETE CASCADE,
    organoid_id VARCHAR(100) NOT NULL,
    t_cell_count INT NOT NULL,
    incubation_hours FLOAT NOT NULL,
    spatial_data JSONB NOT NULL,  -- RAEFISH data
    infiltration_score FLOAT NOT NULL CHECK (infiltration_score BETWEEN 0 AND 1),
    cytotoxicity_score FLOAT NOT NULL CHECK (cytotoxicity_score BETWEEN 0 AND 1),
    success_rate FLOAT NOT NULL CHECK (success_rate BETWEEN 0 AND 1),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_validations_edit ON spatial_validations(edit_id);
CREATE INDEX idx_validations_success ON spatial_validations(success_rate);
CREATE INDEX idx_validations_organoid ON spatial_validations(organoid_id);

-- TED-RV Workflows
CREATE TABLE workflows (
    workflow_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES genomic_profiles(profile_id) ON DELETE CASCADE,
    institution_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL,
    total_cost_usd FLOAT DEFAULT 15000.0,
    elapsed_time_hours FLOAT DEFAULT 0.0,
    success_probability FLOAT DEFAULT 0.85,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_workflow_institution FOREIGN KEY (institution_id) 
        REFERENCES core.institutions(institution_id) ON DELETE CASCADE
);

CREATE INDEX idx_workflows_institution ON workflows(institution_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflows_created ON workflows(created_at DESC);

-- Iteration Feedback
CREATE TABLE iteration_feedback (
    feedback_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES workflows(workflow_id) ON DELETE CASCADE,
    epitope_adjustments JSONB,
    tcr_design_improvements JSONB,
    crispr_parameter_updates JSONB,
    confidence_score FLOAT NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    applied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_feedback_workflow ON iteration_feedback(workflow_id);
CREATE INDEX idx_feedback_confidence ON iteration_feedback(confidence_score);

-- Audit logging trigger
CREATE OR REPLACE FUNCTION tedrv.log_workflow_changes()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit.logs (
        table_name,
        operation,
        record_id,
        old_data,
        new_data,
        user_id,
        institution_id,
        created_at
    ) VALUES (
        TG_TABLE_NAME,
        TG_OP,
        COALESCE(NEW.workflow_id::TEXT, OLD.workflow_id::TEXT),
        to_jsonb(OLD),
        to_jsonb(NEW),
        current_setting('app.current_user_id', TRUE)::UUID,
        COALESCE(NEW.institution_id, OLD.institution_id),
        NOW()
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_workflows
    AFTER INSERT OR UPDATE OR DELETE ON workflows
    FOR EACH ROW EXECUTE FUNCTION tedrv.log_workflow_changes();

-- Row-level security for multi-tenancy
ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;

CREATE POLICY workflows_isolation ON workflows
    USING (institution_id = current_setting('app.current_institution_id')::UUID);

-- Indexes for performance
CREATE INDEX idx_genomic_profiles_hla ON genomic_profiles USING GIN (hla_alleles);
CREATE INDEX idx_neoepitopes_peptide ON neoepitope_predictions(peptide_sequence);
CREATE INDEX idx_spatial_data ON spatial_validations USING GIN (spatial_data);

-- Statistics for query optimization
ANALYZE tedrv.genomic_profiles;
ANALYZE tedrv.neoepitope_predictions;
ANALYZE tedrv.workflows;
```

### 2. Backend Integration

#### Update FastAPI Application

Add TED-RV routes to `src/api/main.py`:

```python
from fastapi import FastAPI
from src.tedrv.api import router as tedrv_router

app = FastAPI(title="TumorTrack Institutional")

# ... existing routes ...

# TED-RV routes
app.include_router(
    tedrv_router,
    prefix="/api/v1/tedrv",
    tags=["TED-RV"],
)
```

#### Create API Router

Create `src/tedrv/api.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID

from .engine import TEDRVEngine
from .models import (
    TEDRVWorkflow,
    PatientGenomicProfile,
    NeoepitopePrediction,
)
from src.auth import get_current_user, require_role

router = APIRouter()
engine = TEDRVEngine()

@router.post("/workflows", response_model=TEDRVWorkflow)
async def create_workflow(
    patient_profile: PatientGenomicProfile,
    institution_id: UUID,
    current_user = Depends(require_role("oncologist")),
):
    """Create a new TED-RV workflow."""
    workflow = engine.create_workflow(patient_profile, str(institution_id))
    # Save to database
    return workflow

@router.post("/workflows/{workflow_id}/module1")
async def run_module1(
    workflow_id: UUID,
    current_user = Depends(require_role("oncologist")),
):
    """Run Module 1: Neoepitope Prediction."""
    # Load workflow from database
    workflow = load_workflow(workflow_id)
    neoepitopes = engine.run_module1_neoepitope_prediction(workflow)
    # Save results
    return {"neoepitopes": neoepitopes}

# ... additional endpoints ...
```

### 3. Environment Configuration

Update `.env`:

```bash
# TED-RV Configuration
TEDRV_ENABLED=true

# AlphaFold 3
ALPHAFOLD3_API_ENDPOINT=https://api.alphafold3.ai/v1
ALPHAFOLD3_API_KEY=your_key_here
ALPHAFOLD3_TIMEOUT=300  # seconds

# Protein LLM
PROTEIN_LLM_API_ENDPOINT=https://api.proteinllm.ai/v1
PROTEIN_LLM_API_KEY=your_key_here

# CRISPR 3.0 Workstation
CRISPR3_WORKSTATION_URL=http://crispr-workstation.local:8001
CRISPR3_API_KEY=your_key_here

# RAEFISH Imager
RAEFISH_IMAGER_URL=http://raefish-imager.local:8002
RAEFISH_API_KEY=your_key_here

# Storage
TEDRV_STRUCTURES_BUCKET=s3://tumortrack-structures/
TEDRV_WES_BUCKET=s3://tumortrack-genomics-encrypted/

# Encryption
GENOMIC_DATA_ENCRYPTION_KEY=your_encryption_key_here

# Performance
TEDRV_MAX_CONCURRENT_WORKFLOWS=10
TEDRV_WORKFLOW_TIMEOUT_HOURS=96  # Allow extra time beyond 72h
```

### 4. Docker Deployment

Create `docker-compose-tedrv.yml`:

```yaml
version: '3.8'

services:
  tedrv-api:
    build:
      context: .
      dockerfile: Dockerfile-tedrv
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - ALPHAFOLD3_API_ENDPOINT=${ALPHAFOLD3_API_ENDPOINT}
      - ALPHAFOLD3_API_KEY=${ALPHAFOLD3_API_KEY}
    volumes:
      - ./src:/app/src
      - structures:/app/structures
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    networks:
      - tumortrack-network

  tedrv-worker:
    build:
      context: .
      dockerfile: Dockerfile-tedrv
    command: celery -A src.tedrv.tasks worker --loglevel=info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    volumes:
      - ./src:/app/src
    depends_on:
      - redis
    networks:
      - tumortrack-network

volumes:
  structures:
    driver: local

networks:
  tumortrack-network:
    external: true
```

### 5. Testing the Integration

#### Unit Tests

Create `tests/tedrv/test_engine.py`:

```python
import pytest
from src.tedrv import TEDRVEngine
from src.tedrv.models import PatientGenomicProfile, HLAAllele

@pytest.fixture
def engine():
    return TEDRVEngine()

@pytest.fixture
def patient_profile():
    return PatientGenomicProfile(
        patient_id="test-patient-001",
        hla_alleles=[HLAAllele("HLA-A*02:01")],
        tumor_mutations={"TP53": ["R248W"]},
    )

def test_create_workflow(engine, patient_profile):
    workflow = engine.create_workflow(
        patient_profile, "test-institution-001"
    )
    assert workflow.workflow_id is not None
    assert workflow.status.value == "pending"

def test_module1_prediction(engine, patient_profile):
    workflow = engine.create_workflow(patient_profile, "test-inst-001")
    neoepitopes = engine.run_module1_neoepitope_prediction(workflow)
    
    assert len(neoepitopes) > 0
    assert neoepitopes[0].rank == 1
    assert 0 <= neoepitopes[0].alphafold3_confidence <= 1
```

#### Integration Test

```bash
# Run complete workflow test
python -m pytest tests/tedrv/test_integration.py -v

# Expected output:
# test_complete_72h_workflow PASSED
# test_module_sequence PASSED
# test_workflow_success_criteria PASSED
```

---

## Production Deployment Checklist

### Security

- [ ] Enable HIPAA-compliant encryption for all genomic data
- [ ] Configure field-level encryption for sequences
- [ ] Set up audit logging for all TED-RV operations
- [ ] Implement MFA for genomic data access
- [ ] Configure VPC isolation for lab equipment APIs
- [ ] Enable rate limiting on expensive endpoints

### Performance

- [ ] Set up Redis cluster for workflow state
- [ ] Configure database connection pooling
- [ ] Enable query result caching
- [ ] Set up CDN for structure files (PDB)
- [ ] Configure load balancing for API servers
- [ ] Monitor API response times (<500ms p95)

### Compliance

- [ ] Document data retention policies (7+ years)
- [ ] Set up automated audit log backups
- [ ] Configure consent tracking integration
- [ ] Implement de-identification pipeline
- [ ] Enable cross-institutional data isolation
- [ ] Set up regulatory reporting exports

### Monitoring

- [ ] Configure Prometheus metrics for TED-RV workflows
- [ ] Set up Grafana dashboards for workflow status
- [ ] Enable alerting for failed validations
- [ ] Monitor AlphaFold 3 API latency
- [ ] Track CRISPR edit quality metrics
- [ ] Monitor spatial validation success rates

---

## Troubleshooting

### Common Issues

**Problem:** AlphaFold 3 predictions timing out

**Solution:**
```bash
# Increase timeout in environment
export ALPHAFOLD3_TIMEOUT=600

# Or switch to local GPU deployment
export ALPHAFOLD3_API_ENDPOINT=http://localhost:8080/af3
```

**Problem:** CRISPR edits exceeding off-target threshold

**Solution:**
```python
# Check CRISPR 3.0 workstation calibration
# Adjust feedback sensitivity
engine.crispr3_url = "http://workstation/recalibrate"
```

**Problem:** Low spatial validation success rates

**Solution:**
```python
# Increase T-cell count or incubation time
validations = engine.run_module3_spatial_validation(
    workflow,
    organoid_id="pdo-001",
    t_cell_count=200000,  # Increased from 100k
)
```

---

## Support & Resources

- **Documentation:** [docs/TEDRV.md](TEDRV.md)
- **Quickstart:** [docs/TEDRV_QUICKSTART.md](TEDRV_QUICKSTART.md)
- **API Reference:** http://localhost:8000/docs
- **GitHub Issues:** https://github.com/ncsound919/Overlay-Bioware/issues
- **Email Support:** support@overlay-bioware.com

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-18  
**Maintainer:** Overlay BioWare Team
