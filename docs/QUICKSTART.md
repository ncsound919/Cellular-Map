# Quick Start Guide

Get NetworkCellularMap v2.0 up and running in 5 minutes!

## Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- OR Node.js 20+ and Python 3.11+ for manual installation

## Option 1: Docker Compose (Recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/ncsound919/Cellular-Map.git
cd Cellular-Map
```

### 2. Start All Services
```bash
docker-compose up -d
```

This will start:
- Neo4j database on port 7687 (browser: 7474)
- Redis cache on port 6379
- Backend API on port 8000
- Frontend on port 3000

### 3. Verify Services
```bash
# Check all services are running
docker-compose ps

# Check backend health
curl http://localhost:8000/health

# Check frontend (in browser)
open http://localhost:3000
```

### 4. Access the Application

- **Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474 (username: neo4j, password: networkology)

### 5. Try the API

#### Diagnose a Patient
```bash
curl -X POST http://localhost:8000/api/v1/networkologist/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "patient_genome": {
      "TP53_mutation": {
        "chr": "17",
        "pos": 7577548,
        "ref": "C",
        "alt": "T"
      }
    },
    "symptoms_multi_organ": ["fatigue", "weight_loss"],
    "patient_id": "TEST001"
  }'
```

#### Analyze a Universal Hub
```bash
curl http://localhost:8000/api/v1/universal_hub/TP53
```

#### Design CRISPR Repair
```bash
curl -X POST http://localhost:8000/api/v1/repair_design/TP53 \
  -H "Content-Type: application/json" \
  -d '{
    "hub_id": "TP53",
    "mutation_ids": ["TP53_R273H"]
  }'
```

### 6. Stop Services
```bash
docker-compose down
```

## Option 2: Manual Installation

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start Neo4j (separate terminal)
# Download from https://neo4j.com/download/
neo4j start

# Start Redis (separate terminal)
redis-server

# Run the backend
uvicorn main:app --reload
```

Backend will be available at http://localhost:8000

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at http://localhost:3000

## Next Steps

### 1. Explore the Dashboard

Visit http://localhost:3000 to see:
- **Universal Mutation Map**: Network visualization of gene interactions
- **Pan-Cellular Hub Radar**: Multi-organ impact analysis
- **Codex Metrics**: Trueness, Flow, and Gravity scores

### 2. Try the API

Interactive API documentation is available at http://localhost:8000/docs

Key endpoints:
- `POST /api/v1/networkologist/diagnose` - Diagnose patient
- `GET /api/v1/universal_hub/{mutation_id}` - Analyze hub
- `POST /api/v1/repair_design/{hub_id}` - Design repair

### 3. Load Sample Data

```python
import requests

# Example diagnosis request
response = requests.post('http://localhost:8000/api/v1/networkologist/diagnose', json={
    "patient_genome": {
        "BRCA1": {"chr": "17", "pos": 41276045, "ref": "C", "alt": "T"},
        "TP53": {"chr": "17", "pos": 7577548, "ref": "C", "alt": "T"}
    },
    "symptoms_multi_organ": ["fatigue", "cognitive_decline", "muscle_weakness"],
    "patient_id": "SAMPLE_001"
})

print(response.json())
```

### 4. Explore Neo4j Database

1. Open http://localhost:7474
2. Login with:
   - Username: `neo4j`
   - Password: `networkology`
3. Try Cypher queries:
   ```cypher
   // Show all nodes
   MATCH (n) RETURN n LIMIT 25
   
   // Find hubs
   MATCH (g:UniversalGene)
   WHERE g.hub_gravity > 0.5
   RETURN g
   ```

## Troubleshooting

### Backend won't start
```bash
# Check if ports are available
lsof -i :8000

# Check logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Frontend won't connect
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check frontend logs
docker-compose logs frontend

# Clear Next.js cache
cd frontend
rm -rf .next
npm run dev
```

### Database connection issues
```bash
# Check Neo4j is running
docker-compose ps neo4j

# Test connection
curl http://localhost:7474

# Check credentials in .env
cat backend/.env
```

### Out of memory
```bash
# Increase Docker memory limit (Docker Desktop)
# Settings > Resources > Memory > 8GB+

# Or reduce replicas in docker-compose.yml
```

## Development Workflow

### Making Changes to Backend

1. Edit files in `backend/app/`
2. Changes auto-reload (if using `--reload` flag)
3. Test with: `curl http://localhost:8000/health`

### Making Changes to Frontend

1. Edit files in `frontend/app/` or `frontend/components/`
2. Changes auto-reload in browser
3. View at: http://localhost:3000

### Adding Dependencies

**Backend:**
```bash
cd backend
pip install new-package
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install new-package
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Kubernetes deployment
- Production best practices
- Security hardening
- Monitoring setup

## Getting Help

- **Documentation**: See `/docs` directory
- **API Docs**: http://localhost:8000/docs
- **Issues**: https://github.com/ncsound919/Cellular-Map/issues

## What's Next?

1. **Integrate Real Data**: Connect to OMIM, GenBank, KEGG APIs
2. **Add Authentication**: Implement user management
3. **Scale Up**: Deploy to Kubernetes cluster
4. **Monitor**: Set up Prometheus and Grafana
5. **Optimize**: Add caching, CDN, database tuning

Happy networking! 🧬🔬
