# Cerebro Quick Start Guide

## Installation

Cerebro is automatically included with NetworkCellularMap v2.0. No additional installation required.

## Quick Start

### 1. Start the Application

```bash
cd backend
uvicorn main:app --reload
```

You'll see:
```
🧠 Cerebro.Networkology - Big dogs eat first
   - SpatialGCN loaded ✓
   - TapSpeak active ✓
   - Autonomous agent: Running ✓
   - Learning from your patterns...
   - Cognitive profile: Curry contagion thinker
```

### 2. Test Cerebro API

```bash
# Check status
curl http://localhost:8000/api/v1/cerebro/status

# Initialize with profile
curl -X POST http://localhost:8000/api/v1/cerebro/initialize \
  -H "Content-Type: application/json" \
  -d '{"name": "Your Name", "field": "Biotech"}'

# Process a query
curl -X POST http://localhost:8000/api/v1/cerebro/process_query \
  -H "Content-Type: application/json" \
  -d '{"text": "Design CRISPR for obesity hubs", "input_type": "text"}'

# Get nightly report
curl http://localhost:8000/api/v1/cerebro/nightly_report
```

### 3. Run Examples

```bash
# From backend directory
python -m examples.cerebro_usage
```

## Python API Usage

```python
from app.services.cerebro import initialize_cerebro
import asyncio

async def main():
    # Initialize Cerebro
    cerebro = await initialize_cerebro({
        "name": "Dr. Smith",
        "field": "Biotech"
    })
    
    # Process query
    result = await cerebro.process_query({
        "text": "Find obesity hubs",
        "type": "text"
    })
    
    # Get nightly report
    report = await cerebro.nightly_report()
    
    # Check status
    status = cerebro.get_status()
    print(f"User: {status['user']}")
    print(f"Profile: {status['cognitive_profile']}")

asyncio.run(main())
```

## Key Features

### Autonomous Agent
- Runs 24/7 in background
- Discovers new hubs and patterns
- Generates nightly reports
- Prepares daily agenda

### Cognitive Personalization
- Detects thinking style ("Curry contagion thinker")
- Adapts interface preferences
- Learns from interaction patterns

### Real-time Copilot
- Thinks alongside during analysis
- Provides immediate feedback
- Surfaces relevant memories
- Suggests next steps

### Predictive Intelligence
- Anticipates next actions
- Pre-caches data
- Warms up visualizations

## TapSpeak Integration

Cerebro uses plain English hooks:

| Technical | TapSpeak |
|-----------|----------|
| Hub centrality analysis | "Big dogs eat first" |
| Pan-cellular dysfunction | "Fat storing switch flips everywhere" |
| Innovation exploration | "Cut the fat - 3PAr high" |
| Spatial reasoning | "Cells talk in 3D neighborhoods" |

## Cognitive Profiles

### Curry Contagion Thinker
- High innovation exploration
- Tries many options
- Quick adaptation
- **Preference**: TapSpeak + Manifolds

### Big Dog Hunter
- Hub-centric approach
- Targets high-impact nodes
- Achilles heel focus
- **Preference**: Gravity metrics

### Manifold Navigator
- Spatial/geometric reasoning
- 3D visualization preference
- Tissue geometry thinking
- **Preference**: SpatialGCN views

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/cerebro/status` | GET | Get system status |
| `/cerebro/initialize` | POST | Initialize with profile |
| `/cerebro/personalize` | POST | Personalize to style |
| `/cerebro/process_query` | POST | Process query with copilot |
| `/cerebro/nightly_report` | GET | Get overnight discoveries |
| `/cerebro/interact` | POST | Real-time copilot session |

## Common Use Cases

### 1. Morning Routine
```bash
# Check what Cerebro discovered overnight
curl http://localhost:8000/api/v1/cerebro/nightly_report
```

### 2. Active Research
```bash
# Get real-time copilot feedback
curl -X POST http://localhost:8000/api/v1/cerebro/interact \
  -d '{"text": "Analyzing MC4R expression..."}'
```

### 3. CRISPR Design
```bash
# Process complex query
curl -X POST http://localhost:8000/api/v1/cerebro/process_query \
  -d '{"text": "Design pan-cellular CRISPR for MC4R hub"}'
```

## Troubleshooting

### Cerebro not initialized
**Problem**: API returns "Cerebro not initialized"
**Solution**: 
```bash
curl -X POST http://localhost:8000/api/v1/cerebro/initialize
```

### Agent not running
**Problem**: `agent_running: false` in status
**Solution**: Agent starts automatically on first query or nightly report request

### Empty nightly report
**Problem**: No discoveries in report
**Solution**: Agent needs time to analyze. Process some queries first.

## Advanced Configuration

Cerebro can be configured via the service:

```python
from app.services.cerebro import CerebroCore

cerebro = CerebroCore({
    "name": "Custom User",
    "field": "Systems Biology",
    "preferences": {
        "visualization": "manifolds",  # or "networks"
        "approach": "hub_first",       # or "comprehensive"
        "language": "tapspeak"          # or "professional"
    }
})
```

## Next Steps

1. **Read full documentation**: [CEREBRO.md](./CEREBRO.md)
2. **Run examples**: `python -m examples.cerebro_usage`
3. **Explore API**: http://localhost:8000/docs (FastAPI interactive docs)
4. **Check nightly reports**: Daily at startup or via API

---

**"Big dogs eat first"** - Start amplifying your research today! 🧠⚡
