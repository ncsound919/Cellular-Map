# NanoStealth Integration Guide

## Overview

This guide provides step-by-step instructions for integrating NanoStealth's open-source tool stack with the TumorTrack Institutional platform.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Core Engine Setup](#core-engine-setup)
3. [Self-Driving Lab Integration](#self-driving-lab-integration)
4. [FHIR & Clinical Integration](#fhir--clinical-integration)
5. [Deployment & Operations](#deployment--operations)
6. [Frontend Integration](#frontend-integration)
7. [Testing & Validation](#testing--validation)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 22.04+ recommended), macOS, or Windows with WSL2
- **Python**: 3.11 or higher
- **Docker**: 20.10+ and Docker Compose 2.0+
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: 20GB available disk space

### Required Accounts & Services

- GitHub account (for CI/CD and container registry)
- PostgreSQL database (local or cloud)
- Redis instance (local or cloud)
- Optional: FHIR server instance (Medplum or HAPI FHIR)

## Core Engine Setup

### 1. Install Python Dependencies

```bash
# Clone the repository
git clone https://github.com/ncsound919/Overlay-Bioware.git
cd Overlay-Bioware

# Create virtual environment
python3.11 -m venv venv-nanostealth
source venv-nanostealth/bin/activate  # On Windows: venv-nanostealth\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements-nanostealth.txt
```

### 2. Install PK/PD Libraries from Source

Some specialized libraries need to be installed from source:

```bash
# PySB - Rule-based modeling
pip install pysb

# PKPy (if available) - Population PK/PD
# git clone https://github.com/pkpy/pkpy.git
# cd pkpy && pip install -e . && cd ..

# For advanced ODE solving
pip install assimulo
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# NanoStealth Configuration
NANOSTEALTH_ENV=development
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/nanostealth
POSTGRES_USER=nanostealth
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=nanostealth

# Redis
REDIS_URL=redis://localhost:6379/0

# FHIR Server
FHIR_SERVER_URL=http://localhost:8080/fhir
FHIR_AUTH_ENABLED=false

# Opentrons (if using lab automation)
OPENTRONS_API_URL=http://opentrons-robot:31950
OPENTRONS_API_KEY=your_api_key_here

# Security
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 4. Initialize Database

```bash
# Start PostgreSQL (if using Docker)
docker run -d \
  --name nanostealth-postgres \
  -e POSTGRES_DB=nanostealth \
  -e POSTGRES_USER=nanostealth \
  -e POSTGRES_PASSWORD=your_secure_password \
  -p 5432:5432 \
  postgres:15-alpine

# Run migrations (once implemented)
# alembic upgrade head
```

### 5. Verify Installation

```bash
# Test Python imports
python -c "import numpy, pandas, scipy, sklearn; print('Core libraries OK')"
python -c "import pysb; print('PySB OK')"
python -c "import fastapi, pydantic; print('FastAPI OK')"

# Run basic tests (once implemented)
# pytest nanostealth/tests/test_core.py -v
```

## Self-Driving Lab Integration

### 1. Opentrons Setup

#### Install Opentrons SDK

```bash
pip install opentrons>=7.0.0
```

#### Connect to Robot

```python
from opentrons import protocol_api

# Example: Test connection
def test_connection():
    # Robot IP address
    robot_ip = "opentrons-robot.local"
    
    # Verify connection
    import requests
    response = requests.get(f"http://{robot_ip}:31950/health")
    print(f"Robot status: {response.json()}")

test_connection()
```

#### Generate Sample Protocol

```python
from nanostealth.protocols import ProtocolBuilder

# Create a protocol builder instance
builder = ProtocolBuilder()

# Define formulation protocol
protocol = builder.create_nanoparticle_synthesis(
    polymer_type="PLGA",
    drug_name="Doxorubicin",
    target_size=100,  # nm
    drug_loading=5.0,  # mg/mL
    surface_modification="PEG"
)

# Export for Opentrons
opentrons_protocol = builder.export_opentrons(protocol)
print(opentrons_protocol)

# Upload to robot
builder.upload_to_robot(opentrons_protocol, robot_ip="opentrons-robot.local")
```

### 2. IvoryOS Integration (Optional)

```bash
# Install IvoryOS (from source)
git clone https://github.com/emergentmethods/ivoryos.git
cd ivoryos
pip install -e .
cd ..

# Configure IvoryOS workflow
# See docs/workflows/nanostealth-optimization.yml
```

## FHIR & Clinical Integration

### 1. FHIR Server Setup

#### Option A: Using HAPI FHIR (Docker)

```bash
# Start HAPI FHIR server
docker run -d \
  --name hapi-fhir \
  -p 8080:8080 \
  -e spring.datasource.url=jdbc:postgresql://host.docker.internal:5432/fhir \
  -e spring.datasource.username=nanostealth \
  -e spring.datasource.password=your_secure_password \
  hapiproject/hapi:latest

# Wait for startup
sleep 30

# Test FHIR server
curl http://localhost:8080/fhir/metadata
```

#### Option B: Using Medplum

```bash
# Install Medplum CLI
npm install -g @medplum/cli

# Initialize Medplum project
medplum init nanostealth-fhir
cd nanostealth-fhir

# Start Medplum server (Docker Compose)
docker-compose up -d

# Test Medplum
curl http://localhost:8103/fhir/R4/metadata
```

### 2. Configure FHIR Client

```python
from fhirclient import client
from nanostealth.fhir import FHIRIntegration

# Initialize FHIR client
settings = {
    'app_id': 'nanostealth',
    'api_base': 'http://localhost:8080/fhir'
}
smart = client.FHIRClient(settings=settings)

# Initialize NanoStealth FHIR integration
fhir_integration = FHIRIntegration(smart)

# Create a medication administration record
med_admin = fhir_integration.create_medication_administration(
    patient_id="Patient/123",
    medication_code="doxorubicin-nanoparticle",
    dose_quantity=50.0,
    dose_unit="mg",
    formulation_details={
        "particle_size": 100,
        "surface_chemistry": "PEG",
        "drug_loading": 5.0
    }
)
```

### 3. Open Health Stack Integration

```bash
# Install Open Health Stack FHIR SDK (if available)
# pip install open-health-fhir-sdk

# Or use fhir.resources for resource models
pip install fhir.resources

# Example usage
from fhir.resources.observation import Observation
from fhir.resources.quantity import Quantity

# Create PK observation
pk_obs = Observation(
    status="final",
    code={"coding": [{"system": "http://loinc.org", "code": "PK-CONCENTRATION"}]},
    subject={"reference": "Patient/123"},
    valueQuantity=Quantity(value=12.5, unit="ng/mL", system="http://unitsofmeasure.org", code="ng/mL")
)
```

## Deployment & Operations

### 1. Docker Deployment

```bash
# Build the Docker image
docker build -t nanostealth:latest -f Dockerfile-nanostealth .

# Start all services with Docker Compose
docker-compose -f docker-compose-nanostealth.yml up -d

# Verify services are running
docker-compose -f docker-compose-nanostealth.yml ps

# View logs
docker-compose -f docker-compose-nanostealth.yml logs -f nanostealth-api

# Access API documentation
# Open browser: http://localhost:8001/docs
```

### 2. CI/CD Setup

The GitHub Actions workflow is automatically configured in `.github/workflows/nanostealth-ci-cd.yml`.

#### Enable Self-Hosted Runner (for Lab Deployment)

```bash
# On your lab machine/Raspberry Pi
mkdir -p ~/actions-runner && cd ~/actions-runner

# Download runner (adjust version as needed)
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure (follow prompts, use labels: lab, opentrons)
./config.sh --url https://github.com/ncsound919/Overlay-Bioware --token YOUR_RUNNER_TOKEN

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start
```

### 3. LabOps Tools Setup (Optional)

#### Nextcloud for Data Sharing

```bash
# Install Nextcloud (Docker)
docker run -d \
  --name nextcloud \
  -p 8082:80 \
  -v nextcloud_data:/var/www/html \
  nextcloud:latest
```

#### Mattermost for Communication

```bash
# Install Mattermost (Docker Compose)
git clone https://github.com/mattermost/docker
cd docker
docker-compose -f docker-compose.yml up -d
```

#### JupyterHub for Analysis

```bash
# Install JupyterHub
pip install jupyterhub jupyterlab notebook

# Start JupyterHub
jupyterhub --ip 0.0.0.0 --port 8000
```

## Frontend Integration

### 1. Add NanoStealth UI Components to TumorTrack

```bash
# Navigate to frontend directory (if exists)
cd frontend

# Install visualization libraries
npm install plotly.js react-plotly.js vega vega-lite react-vega

# Or with yarn
yarn add plotly.js react-plotly.js vega vega-lite react-vega
```

### 2. Create NanoStealth Dashboard Component

```typescript
// components/NanoStealth/OptimizationDashboard.tsx
import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

interface MetricsData {
  trueness: number;
  flow: number;
  toxicity: number;
}

export const OptimizationDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricsData | null>(null);

  useEffect(() => {
    // Fetch metrics from API
    fetch('/api/v1/nanostealth/metrics')
      .then(res => res.json())
      .then(data => setMetrics(data));
  }, []);

  if (!metrics) return <div>Loading...</div>;

  return (
    <div className="nanostealth-dashboard">
      <h1>NanoStealth Optimization Dashboard</h1>
      
      {/* Trueness Gauge */}
      <Plot
        data={[{
          type: 'indicator',
          mode: 'gauge+number',
          value: metrics.trueness,
          gauge: { axis: { range: [0, 1] } }
        }]}
        layout={{ title: 'Trueness (Targeting Accuracy)' }}
      />
      
      {/* Add more visualizations */}
    </div>
  );
};
```

### 3. Add Routes

```typescript
// pages/nanostealth/index.tsx
import { OptimizationDashboard } from '@/components/NanoStealth/OptimizationDashboard';

export default function NanoStealthPage() {
  return <OptimizationDashboard />;
}
```

## Testing & Validation

### 1. Run Unit Tests

```bash
# Activate virtual environment
source venv-nanostealth/bin/activate

# Run all tests
pytest nanostealth/tests/ -v

# Run specific test suite
pytest nanostealth/tests/test_pk_models.py -v

# Run with coverage
pytest nanostealth/tests/ --cov=nanostealth --cov-report=html
```

### 2. Validate PK/PD Models

```bash
# Run model validation script
python -m nanostealth.pk_models.validate

# Run benchmarks
python -m nanostealth.benchmarks.pk_performance
```

### 3. Integration Testing

```bash
# Start test environment
docker-compose -f docker-compose-nanostealth.yml up -d

# Run integration tests
pytest nanostealth/tests/integration/ -v

# Stop test environment
docker-compose -f docker-compose-nanostealth.yml down
```

## Troubleshooting

### Common Issues

#### 1. PK/PD Library Import Errors

**Problem**: `ModuleNotFoundError: No module named 'pkpy'`

**Solution**: Some libraries may not be on PyPI. Install from source:
```bash
git clone https://github.com/pkpy/pkpy.git
cd pkpy
pip install -e .
```

#### 2. Opentrons Connection Failed

**Problem**: Cannot connect to Opentrons robot

**Solution**:
- Verify robot is powered on and connected to network
- Check robot IP address: `ping opentrons-robot.local`
- Ensure firewall allows port 31950
- Test with: `curl http://ROBOT_IP:31950/health`

#### 3. FHIR Server Authentication Issues

**Problem**: 401 Unauthorized when accessing FHIR resources

**Solution**:
- Check FHIR server authentication settings
- Verify OAuth2 credentials (if enabled)
- For development, disable authentication in FHIR server config

#### 4. Docker Container Exits Immediately

**Problem**: NanoStealth container exits with error

**Solution**:
```bash
# Check logs
docker logs nanostealth-api

# Common causes:
# - Database connection failed: verify DATABASE_URL
# - Missing environment variables: check .env file
# - Port conflict: change port mapping in docker-compose

# Debug mode
docker run -it --rm \
  -e DATABASE_URL=postgresql://... \
  nanostealth:latest \
  /bin/bash
```

#### 5. NumPy/SciPy Installation Failures

**Problem**: Build errors when installing NumPy/SciPy

**Solution**:
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3-dev build-essential gfortran libopenblas-dev liblapack-dev

# macOS
brew install openblas lapack

# Retry installation
pip install numpy scipy
```

## Next Steps

1. **Customize PK Models**: Extend `nanostealth.pk_models` with your specific nanocarrier types
2. **Create Lab Protocols**: Develop Opentrons protocols in `nanostealth.protocols`
3. **Integrate with TumorTrack**: Link nanocarrier data to tumor dynamics models
4. **Deploy to Production**: Follow deployment guide for production environment
5. **Train Models**: Collect real data and retrain prediction models

## Support & Resources

- **Documentation**: See `docs/NANOSTEALTH.md` for detailed architecture
- **Configuration**: See `config/nanostealth.json` for all settings
- **Issues**: Report bugs at https://github.com/ncsound919/Overlay-Bioware/issues
- **Community**: Join discussions on project forums

---

**Last Updated**: 2025-12-18  
**Version**: 1.0.0
