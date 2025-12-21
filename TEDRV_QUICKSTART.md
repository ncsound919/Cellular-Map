# TED-RV Quickstart Guide

## Getting Started with TED-RV

This guide walks you through running your first TED-RV workflow for personalized T-cell therapy design.

## Prerequisites

### Software Requirements

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optional, for containerized deployment)

### Hardware Requirements

- **Minimum:** 16GB RAM, 4-core CPU
- **Recommended:** 32GB RAM, 8-core CPU, GPU (for local AlphaFold 3)
- **Production:** 200 sq ft lab with CRISPR 3.0 workstation + RAEFISH imager

### API Access

- AlphaFold 3 API key (cloud or self-hosted)
- Protein LLM API key (optional, enhances predictions)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements-tedrv.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/tumortrack

# Redis
REDIS_URL=redis://localhost:6379/0

# TED-RV APIs
ALPHAFOLD3_API_ENDPOINT=https://api.alphafold3.ai/v1
ALPHAFOLD3_API_KEY=your_af3_api_key_here
PROTEIN_LLM_API_ENDPOINT=https://api.proteinllm.ai/v1
PROTEIN_LLM_API_KEY=your_llm_api_key_here

# Lab Equipment (local deployment)
CRISPR3_WORKSTATION_URL=http://localhost:8001/crispr3
RAEFISH_IMAGER_URL=http://localhost:8002/raefish

# Security
ENCRYPTION_KEY=your_encryption_key_here
JWT_SECRET=your_jwt_secret_here
```

### 3. Initialize Database Schema

```bash
python -m src.tedrv.scripts.init_db
```

## Quick Start Example

### Example 1: Complete 72-Hour Workflow

```python
from src.tedrv import TEDRVEngine
from src.tedrv.models import PatientGenomicProfile, HLAAllele

# Initialize engine
engine = TEDRVEngine(
    alphafold3_api_endpoint="https://api.alphafold3.ai/v1",
    crispr3_workstation_url="http://localhost:8001/crispr3",
    raefish_imager_url="http://localhost:8002/raefish",
    protein_llm_endpoint="https://api.proteinllm.ai/v1",
)

# Create patient genomic profile (de-identified)
patient_profile = PatientGenomicProfile(
    patient_id="patient-uuid-12345",
    hla_alleles=[
        HLAAllele("HLA-A*02:01"),
        HLAAllele("HLA-A*24:02"),
        HLAAllele("HLA-B*07:02"),
        HLAAllele("HLA-C*07:02"),
    ],
    tumor_mutations={
        "TP53": ["R248W", "R273H"],
        "KRAS": ["G12D"],
        "EGFR": ["L858R"],
    },
    tumor_wes_path="s3://encrypted/patient-12345/tumor.vcf.gz",
    normal_wes_path="s3://encrypted/patient-12345/normal.vcf.gz",
    tumor_burden_mb=15.2,
)

# Run complete workflow (72 hours)
workflow = engine.run_complete_workflow(
    patient_profile=patient_profile,
    institution_id="institution-uuid-001",
    organoid_id="pdo-12345",
)

# Check results
print(f"Workflow ID: {workflow.workflow_id}")
print(f"Status: {workflow.status}")
print(f"Elapsed time: {workflow.elapsed_time_hours} hours")
print(f"Total cost: ${workflow.total_cost_usd:,.2f}")
print(f"Success probability: {workflow.success_probability:.1%}")

# Top neoepitopes
print("\nTop 3 Neoepitopes:")
for epitope in workflow.neoepitopes[:3]:
    print(f"  Rank {epitope.rank}: {epitope.peptide_sequence}")
    print(f"    HLA: {epitope.hla_allele}")
    print(f"    Binding affinity: {epitope.binding_affinity_nm:.1f} nM")
    print(f"    AlphaFold3 confidence: {epitope.alphafold3_confidence:.3f}")
    print(f"    Immunogenicity: {epitope.immunogenicity_score:.3f}")

# Validation results
print("\nSpatial Validation Results:")
for validation in workflow.validations:
    print(f"  Edit ID: {validation.edit_id}")
    print(f"    Infiltration: {validation.infiltration_score:.1%}")
    print(f"    Cytotoxicity: {validation.cytotoxicity_score:.1%}")
    print(f"    Success rate: {validation.success_rate:.1%}")
    print(f"    Status: {'✓ PASS' if validation.success_rate >= 0.85 else '✗ FAIL'}")

# Overall success
if workflow.is_successful():
    print("\n✓ Workflow SUCCESSFUL - Ready for clinical validation")
else:
    print("\n✗ Workflow needs optimization")
```

### Example 2: Step-by-Step Module Execution

```python
from src.tedrv import TEDRVEngine
from src.tedrv.models import PatientGenomicProfile, HLAAllele, WorkflowStatus

engine = TEDRVEngine()

# Create patient profile
patient_profile = PatientGenomicProfile(
    patient_id="patient-uuid-67890",
    hla_alleles=[
        HLAAllele("HLA-A*02:01"),
        HLAAllele("HLA-B*07:02"),
    ],
    tumor_mutations={
        "TP53": ["R248W"],
        "PIK3CA": ["H1047R"],
    },
    tumor_burden_mb=12.5,
)

# Create workflow
workflow = engine.create_workflow(
    patient_profile=patient_profile,
    institution_id="institution-uuid-001",
)

# Module 1: Neoepitope Prediction (12 hours)
print("Running Module 1: Neoepitope Prediction...")
neoepitopes = engine.run_module1_neoepitope_prediction(workflow, top_n=10)
print(f"  Predicted {len(neoepitopes)} neoepitopes")
print(f"  Elapsed time: {workflow.elapsed_time_hours} hours")

# Module 2: CRISPR 3.0 Engineering (24 hours)
print("\nRunning Module 2: CRISPR 3.0 T-Cell Engineering...")
crispr_edits = engine.run_module2_crispr_engineering(workflow)
print(f"  Designed {len(crispr_edits)} CRISPR edits")
print(f"  Elapsed time: {workflow.elapsed_time_hours} hours")

# Check CRISPR quality
for edit in crispr_edits:
    print(f"    Edit {edit.edit_id}:")
    print(f"      On-target: {edit.on_target_efficiency:.1%}")
    print(f"      Off-target: {edit.off_target_rate:.3%}")
    print(f"      Cell viability: {edit.cell_viability:.1%}")

# Module 3: Spatial Validation (36 hours)
print("\nRunning Module 3: Spatial Validation...")
validations = engine.run_module3_spatial_validation(
    workflow,
    organoid_id="pdo-67890",
    t_cell_count=100000,
)
print(f"  Completed {len(validations)} validations")
print(f"  Elapsed time: {workflow.elapsed_time_hours} hours")

# Module 4: AI Iteration
print("\nRunning Module 4: AI Iteration...")
feedback = engine.run_module4_ai_iteration(workflow)
print(f"  Generated feedback with confidence: {feedback.confidence_score:.1%}")
print(f"  Status: {workflow.status}")
```

### Example 3: Accessing Results via API

```bash
# Create workflow
curl -X POST http://localhost:8000/api/v1/tedrv/workflows \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_profile": {
      "patient_id": "patient-uuid-12345",
      "hla_alleles": ["HLA-A*02:01", "HLA-B*07:02"],
      "tumor_mutations": {
        "TP53": ["R248W"],
        "KRAS": ["G12D"]
      }
    },
    "institution_id": "institution-uuid-001"
  }'

# Response: {"workflow_id": "workflow-uuid-abc123", "status": "pending"}

# Run complete workflow
curl -X POST http://localhost:8000/api/v1/tedrv/workflows/workflow-uuid-abc123/complete \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{"organoid_id": "pdo-12345"}'

# Get workflow status
curl http://localhost:8000/api/v1/tedrv/workflows/workflow-uuid-abc123 \
  -H "Authorization: Bearer $JWT_TOKEN"

# Download AlphaFold 3 structure
curl http://localhost:8000/api/v1/tedrv/structures/epitope-uuid-xyz.pdb \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -o structure.pdb
```

## Understanding the Results

### Neoepitope Prediction Metrics

- **Binding Affinity (nM):** Lower is better. <50 nM = strong binder, 50-500 nM = moderate, >500 nM = weak
- **AlphaFold3 Confidence:** 0-1 scale. >0.85 = high confidence, 0.7-0.85 = moderate, <0.7 = low
- **Immunogenicity Score:** 0-1 scale. >0.8 = highly immunogenic, 0.6-0.8 = moderate, <0.6 = weak
- **Cross-Reactivity Risk:** 0-1 scale. <0.1 = low risk, 0.1-0.3 = moderate, >0.3 = high

### CRISPR Edit Quality

- **On-Target Efficiency:** Should be >95% for clinical use
- **Off-Target Rate:** Must be <0.2% (CRISPR 3.0 threshold)
- **Cell Viability:** Should be >99% for sufficient T-cell numbers

### Spatial Validation Success

- **Infiltration Score:** >0.7 indicates good T-cell penetration
- **Cytotoxicity Score:** >0.8 indicates strong tumor killing
- **Overall Success Rate:** >0.85 target for clinical advancement

## Troubleshooting

### Common Issues

**Issue: AlphaFold 3 API timeout**
```python
# Solution: Increase timeout or use local GPU
engine = TEDRVEngine(
    alphafold3_api_endpoint="http://localhost:8080/af3",  # Local server
)
```

**Issue: Low neoepitope binding affinity**
```python
# Solution: Lower threshold or expand HLA typing
neoepitopes = engine.run_module1_neoepitope_prediction(
    workflow,
    top_n=20,  # Get more candidates
)
```

**Issue: CRISPR off-target rate too high**
```python
# Solution: Adjust CRISPR 3.0 feedback parameters
# This would be configured in the CRISPR 3.0 workstation
```

**Issue: Low spatial validation success**
```python
# Solution: Increase T-cell count or incubation time
validations = engine.run_module3_spatial_validation(
    workflow,
    organoid_id="pdo-12345",
    t_cell_count=200000,  # Double the cells
)
```

## Performance Optimization

### For Large-Scale Deployment

```python
# Use async processing for multiple patients
import asyncio

async def process_patient(patient_profile, institution_id):
    engine = TEDRVEngine()
    workflow = await engine.run_complete_workflow_async(
        patient_profile=patient_profile,
        institution_id=institution_id,
        organoid_id=f"pdo-{patient_profile.patient_id}",
    )
    return workflow

# Process 10 patients concurrently
patients = [create_patient_profile(i) for i in range(10)]
workflows = await asyncio.gather(*[
    process_patient(p, "institution-001") for p in patients
])
```

### Caching for Repeated Analyses

```python
# Cache AlphaFold 3 predictions for common HLA alleles
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_af3_prediction(peptide, hla_allele):
    return engine._simulate_alphafold3_prediction(peptide, hla_allele)
```

## Next Steps

1. **Review Full Documentation:** [docs/TEDRV.md](TEDRV.md)
2. **Explore Integration:** [docs/TEDRV_INTEGRATION.md](TEDRV_INTEGRATION.md)
3. **Check API Reference:** http://localhost:8000/docs (OpenAPI)
4. **Run Example Workflows:** See `examples/tedrv_workflows.py`
5. **Set Up Lab Equipment:** [docs/TEDRV_LAB_SETUP.md](TEDRV_LAB_SETUP.md)

## Support

For questions or issues:
- **Documentation:** `/docs/TEDRV.md`
- **Issues:** GitHub Issues
- **Email:** support@overlay-bioware.com

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-18
