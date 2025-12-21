# NanoStealth Quick Start Guide

Get NanoStealth up and running in 15 minutes!

## Prerequisites

- Docker and Docker Compose installed
- 8GB RAM minimum
- 10GB free disk space

## Option 1: Docker Quick Start (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/ncsound919/Overlay-Bioware.git
cd Overlay-Bioware
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env.nanostealth

# Edit with your settings (optional for quick start)
# nano .env.nanostealth
```

### 3. Start All Services

```bash
# Start the complete stack
docker-compose -f docker-compose-nanostealth.yml up -d

# Wait for services to initialize (about 30 seconds)
sleep 30

# Check status
docker-compose -f docker-compose-nanostealth.yml ps
```

### 4. Verify Installation

```bash
# Check API health
curl http://localhost:8001/api/v1/nanostealth/health

# Expected response:
# {"status": "healthy", "version": "1.0.0"}

# Access API documentation
# Open browser: http://localhost:8001/docs
```

### 5. Run Your First Optimization

```bash
# Simple curl example
curl -X POST http://localhost:8001/api/v1/nanostealth/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "target": {
      "trueness": 0.70,
      "flow": 24.0,
      "toxicity": 0.20
    },
    "patient": {
      "tumor_volume": 15.0,
      "liver_function": 0.9,
      "weight": 70.0
    }
  }'
```

## Option 2: Local Python Development

### 1. Set Up Python Environment

```bash
# Clone repository
git clone https://github.com/ncsound919/Overlay-Bioware.git
cd Overlay-Bioware

# Create virtual environment
python3.11 -m venv venv-nanostealth
source venv-nanostealth/bin/activate  # On Windows: venv-nanostealth\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements-nanostealth.txt
```

### 2. Start Dependencies (Docker)

```bash
# Start only PostgreSQL and Redis
docker run -d --name nanostealth-postgres \
  -e POSTGRES_DB=nanostealth \
  -e POSTGRES_USER=nanostealth \
  -e POSTGRES_PASSWORD=dev_password \
  -p 5432:5432 \
  postgres:15-alpine

docker run -d --name nanostealth-redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 3. Configure Environment

```bash
# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://nanostealth:dev_password@localhost:5432/nanostealth
REDIS_URL=redis://localhost:6379/0
NANOSTEALTH_ENV=development
LOG_LEVEL=debug
EOF
```

### 4. Initialize Database (when backend is ready)

```bash
# Run migrations (placeholder - implement when backend is ready)
# alembic upgrade head

# Or create tables manually
# python -m nanostealth.db.init
```

### 5. Start Development Server

```bash
# Start NanoStealth API (when implemented)
# uvicorn nanostealth.main:app --reload --port 8001

# For now, verify imports work
python -c "import numpy, pandas, scipy, sklearn, pysb; print('✓ All core libraries installed')"
```

## Option 3: Quick Test Without Backend

If you just want to explore the PK/PD modeling capabilities:

```bash
# Install dependencies
pip install numpy scipy pysb matplotlib

# Create a simple PK simulation script
cat > test_pk.py << 'EOF'
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Simple two-compartment PK model
def pk_model(y, t, dose, ka, ke, k12, k21, V1):
    """Two-compartment model with first-order absorption"""
    Aa, A1, A2 = y  # Absorption, Central, Peripheral
    
    dAa = -ka * Aa
    dA1 = ka * Aa - ke * A1 - k12 * A1 + k21 * A2
    dA2 = k12 * A1 - k21 * A2
    
    return [dAa, dA1, dA2]

# Parameters for a nanoparticle
dose = 50.0  # mg
ka = 0.5     # absorption rate (h^-1)
ke = 0.03    # elimination rate (h^-1) - slow for nanoparticles
k12 = 0.1    # central to peripheral (h^-1)
k21 = 0.05   # peripheral to central (h^-1)
V1 = 5.0     # volume of central compartment (L)

# Initial conditions
y0 = [dose, 0, 0]  # All drug in absorption compartment

# Time points (0 to 72 hours)
t = np.linspace(0, 72, 500)

# Solve ODE
solution = odeint(pk_model, y0, t, args=(dose, ka, ke, k12, k21, V1))

# Calculate concentration (mg/L)
concentration = solution[:, 1] / V1

# Plot
plt.figure(figsize=(10, 6))
plt.plot(t, concentration, 'b-', linewidth=2)
plt.xlabel('Time (hours)', fontsize=12)
plt.ylabel('Plasma Concentration (mg/L)', fontsize=12)
plt.title('Nanoparticle PK Profile (Two-Compartment Model)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.axhline(y=concentration.max() * 0.5, color='r', linestyle='--', 
            label=f'Half-max concentration')

# Calculate half-life
half_life = np.log(2) / ke
plt.text(half_life, concentration.max() * 0.6, 
         f'Half-life: {half_life:.1f} hours', fontsize=10)

plt.legend()
plt.tight_layout()
plt.savefig('nanoparticle_pk_profile.png', dpi=150)
print(f"✓ PK profile saved to nanoparticle_pk_profile.png")
print(f"✓ Half-life: {half_life:.1f} hours")
print(f"✓ Cmax: {concentration.max():.2f} mg/L")
EOF

# Run the simulation
python test_pk.py

# View the plot
# Open nanoparticle_pk_profile.png in your image viewer
```

## Common Tasks

### View Logs

```bash
# Docker logs
docker-compose -f docker-compose-nanostealth.yml logs -f nanostealth-api

# Filter specific service
docker-compose -f docker-compose-nanostealth.yml logs -f postgres
```

### Restart Services

```bash
# Restart specific service
docker-compose -f docker-compose-nanostealth.yml restart nanostealth-api

# Restart all
docker-compose -f docker-compose-nanostealth.yml restart
```

### Stop Services

```bash
# Stop all services
docker-compose -f docker-compose-nanostealth.yml down

# Stop and remove volumes (WARNING: deletes data!)
docker-compose -f docker-compose-nanostealth.yml down -v
```

### Access Database

```bash
# Connect to PostgreSQL
docker exec -it nanostealth-postgres psql -U nanostealth -d nanostealth

# Run a query
# SELECT * FROM formulations LIMIT 10;
```

### Access Redis

```bash
# Connect to Redis CLI
docker exec -it nanostealth-redis redis-cli

# Check keys
# KEYS *
# GET some_key
```

## Next Steps

1. **Read the Documentation**
   - Architecture: [docs/NANOSTEALTH.md](docs/NANOSTEALTH.md)
   - Integration Guide: [docs/NANOSTEALTH_INTEGRATION.md](docs/NANOSTEALTH_INTEGRATION.md)
   - NBA Translation: [docs/NANOSTEALTH_NBA_TRANSLATION.md](docs/NANOSTEALTH_NBA_TRANSLATION.md)

2. **Explore the API**
   - Interactive docs: http://localhost:8001/docs
   - OpenAPI spec: http://localhost:8001/openapi.json

3. **Configure FHIR Integration**
   - See integration guide for FHIR server setup
   - Configure FHIR_SERVER_URL in .env

4. **Set Up Lab Automation**
   - Install Opentrons SDK: `pip install opentrons`
   - Configure OPENTRONS_API_URL in .env
   - See integration guide for protocol examples

5. **Run Tests**
   ```bash
   # Install test dependencies
   pip install pytest pytest-asyncio pytest-cov
   
   # Run tests (when implemented)
   # pytest nanostealth/tests/ -v
   ```

6. **Contribute**
   - Fork the repository
   - Create a feature branch
   - Submit a pull request

## Troubleshooting

### Port Already in Use

```bash
# Change ports in docker-compose-nanostealth.yml
# Example: Change 8001:8001 to 8002:8001
```

### Database Connection Failed

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check logs
docker logs nanostealth-postgres

# Verify connection string in .env
```

### Import Errors

```bash
# Make sure virtual environment is activated
source venv-nanostealth/bin/activate

# Reinstall dependencies
pip install -r requirements-nanostealth.txt
```

### Docker Build Failed

```bash
# Clear Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose -f docker-compose-nanostealth.yml build --no-cache
```

## Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: https://github.com/ncsound919/Overlay-Bioware/issues
- **Discussions**: https://github.com/ncsound919/Overlay-Bioware/discussions

## Development Workflow

```bash
# 1. Make changes to code
# nano nanostealth/pk_models.py

# 2. Run linter
# black nanostealth/
# flake8 nanostealth/

# 3. Run tests
# pytest nanostealth/tests/ -v

# 4. Commit changes
# git add .
# git commit -m "Add new PK model"

# 5. Push to GitHub
# git push origin feature/new-pk-model
```

---

**Happy coding!** 🚀

For detailed setup instructions, see [NANOSTEALTH_INTEGRATION.md](NANOSTEALTH_INTEGRATION.md)
