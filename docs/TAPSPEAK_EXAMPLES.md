# TapSpeak Usage Examples

This document demonstrates how to use the TapSpeak translation system in the NetworkCellularMap application.

## Backend (Python)

### Using the TapSpeak Engine

```python
from app.services.tapspeak import get_tapspeak_engine

# Get the engine
engine = get_tapspeak_engine()

# Get all core concepts
core_concepts = engine.get_all_concepts(category="core_concepts")
for concept in core_concepts:
    print(f"{concept.tap_speak} -> {concept.professional}")

# Search by tags
hub_concepts = engine.search(tags=["hubs", "gravity"])
for concept in hub_concepts:
    print(f"ID {concept.id}: {concept.tap_speak}")

# Translate a technical term
translation = engine.translate_term("Hub centrality")
if translation:
    print(f"TapSpeak: {translation.tap_speak}")
    print(f"Hook: {translation.hooks}")
    print(f"ESAT: {translation.confidence.esat}%")

# Get dashboard data
dashboard = engine.get_dashboard_data()
print(f"Total: {dashboard.total_translations}")
print(f"Avg ESAT: {dashboard.average_confidence.esat}")
```

### Using the API Endpoints

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Get all concepts
response = requests.get(f"{BASE_URL}/tapspeak/concepts")
concepts = response.json()

# Get concepts by category
response = requests.get(f"{BASE_URL}/tapspeak/concepts?category=core_concepts")
core_concepts = response.json()

# Search with filters
search_request = {
    "query": "hub",
    "tags": ["gravity", "hubs"],
    "min_esat": 80.0,
    "min_cep": 85.0
}
response = requests.post(f"{BASE_URL}/tapspeak/search", json=search_request)
results = response.json()

# Translate a technical term
translate_request = {
    "technical_term": "CRISPR-Cas9",
    "domain": "biotech"
}
response = requests.post(f"{BASE_URL}/tapspeak/translate", json=translate_request)
translation = response.json()
print(f"TapSpeak: {translation['tap_speak']}")

# Get dashboard data
response = requests.get(f"{BASE_URL}/tapspeak/dashboard")
dashboard = response.json()
print(f"Total translations: {dashboard['total_translations']}")
```

## Frontend (TypeScript/React)

### Using the TapSpeak API Client

```typescript
import { tapspeakAPI } from '@/lib/tapspeak-api';

// Get all concepts
const concepts = await tapspeakAPI.getConcepts();

// Get concepts by category
const coreConcepts = await tapspeakAPI.getConcepts('core_concepts');

// Search with filters
const results = await tapspeakAPI.search({
  query: 'hub',
  tags: ['gravity', 'hubs'],
  min_esat: 80.0,
  min_cep: 85.0
});

// Translate a technical term
try {
  const translation = await tapspeakAPI.translateTerm({
    technical_term: 'Hub centrality',
    domain: 'biotech'
  });
  console.log('TapSpeak:', translation.tap_speak);
} catch (error) {
  console.error('Translation not found:', error);
}

// Get dashboard data
const dashboard = await tapspeakAPI.getDashboardData();
console.log('Total:', dashboard.total_translations);
console.log('Avg ESAT:', dashboard.average_confidence.esat);

// Get statistics
const stats = await tapspeakAPI.getStats();
console.log('Tags:', stats.tags);
```

### Using TapSpeak Components

```tsx
import TapSpeakCard from '@/components/dashboard/TapSpeakCard';
import TapSpeakDashboard from '@/components/dashboard/TapSpeakDashboard';

// Single card
function MyPage() {
  const translation = {
    id: 5,
    tap_speak: "Big dogs eat first (high Gravity)",
    professional: "Hub centrality + attractiveness index",
    operational: "Scale-free network hubs control 80% system state",
    translational: "Fix the kingpin one shot cures whole disease",
    confidence: { esat: 90.0, cep: 95.0 },
    hooks: "Elephant in room pulls whole circus",
    tags: ["hubs", "achilles", "gravity", "codex"]
  };

  return <TapSpeakCard translation={translation} defaultView="common" />;
}

// Full dashboard
function TapSpeakPage() {
  return <TapSpeakDashboard />;
}
```

## cURL Examples

```bash
# Get all concepts
curl http://localhost:8000/api/v1/tapspeak/concepts

# Get concepts by category
curl "http://localhost:8000/api/v1/tapspeak/concepts?category=core_concepts"

# Search
curl -X POST http://localhost:8000/api/v1/tapspeak/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "hub",
    "min_esat": 80.0
  }'

# Translate
curl -X POST http://localhost:8000/api/v1/tapspeak/translate \
  -H "Content-Type: application/json" \
  -d '{
    "technical_term": "Hub centrality",
    "domain": "biotech"
  }'

# Get dashboard
curl http://localhost:8000/api/v1/tapspeak/dashboard

# Get stats
curl http://localhost:8000/api/v1/tapspeak/stats

# Get all tags
curl http://localhost:8000/api/v1/tapspeak/tags

# Get concept by ID
curl http://localhost:8000/api/v1/tapspeak/concept/5
```

## Integration Examples

### Adding TapSpeak to Network Analysis

```python
from app.services.tapspeak import get_tapspeak_engine
from app.services.network import NetworkService

# Get network hub analysis
network_service = NetworkService()
hub_analysis = network_service.analyze_hub("TP53")

# Translate hub metrics to TapSpeak
tapspeak = get_tapspeak_engine()
gravity_translation = tapspeak.translate_term("Hub centrality")

# Combine technical and TapSpeak explanations
response = {
    "technical": {
        "hub_id": "TP53",
        "degree_centrality": hub_analysis.degree_centrality,
        "gravity_score": hub_analysis.gravity_score
    },
    "tapspeak": {
        "plain_english": gravity_translation.tap_speak,
        "memory_hook": gravity_translation.hooks,
        "real_world_impact": gravity_translation.translational
    }
}
```

### Adding TapSpeak to Diagnosis Results

```python
from app.services.networkologist import diagnose_patient
from app.services.tapspeak import get_tapspeak_engine

# Perform diagnosis
diagnosis = diagnose_patient(patient_data)

# Add TapSpeak translations
tapspeak = get_tapspeak_engine()

# Explain Codex scores in plain English
codex_explanations = {
    "trueness": tapspeak.translate_term("Trueness metric"),
    "flow": tapspeak.translate_term("Flow metric"),
    "gravity": tapspeak.translate_term("Gravity metric")
}

diagnosis["tapspeak_explanations"] = codex_explanations
```

## Output Examples

### Core Concept Example

```json
{
  "id": 5,
  "tap_speak": "Big dogs eat first (high Gravity)",
  "professional": "Hub centrality + attractiveness index",
  "operational": "Scale-free network hubs control 80% system state",
  "translational": "Fix the kingpin one shot cures whole disease",
  "confidence": {
    "esat": 90.0,
    "cep": 95.0
  },
  "hooks": "Elephant in room pulls whole circus",
  "tags": ["hubs", "achilles", "gravity", "codex"]
}
```

### BBTech Mapping Example

```json
{
  "id": 32,
  "tap_speak": "Big dog gravity",
  "professional": "Gravity = hub attractiveness",
  "operational": "LeBron ball dominance = network hub control",
  "translational": "Fix superstar gene cures team",
  "confidence": {
    "esat": 90.0,
    "cep": 95.0
  },
  "hooks": "GOAT gene rules the court",
  "tags": ["bbtech", "gravity", "scale_free"]
}
```

### Dashboard Data Example

```json
{
  "core_concepts": [...],
  "workflow_steps": [...],
  "codex_metrics": [...],
  "bbtech_mappings": [...],
  "total_translations": 13,
  "average_confidence": {
    "esat": 82.3,
    "cep": 87.3
  }
}
```

## Tips

1. **Use search for discovery**: Search by tags or query to find relevant translations
2. **Validate confidence**: Check ESAT/CEP scores to ensure quality
3. **Combine views**: Toggle between common and expert views for different audiences
4. **Cache translations**: Dashboard data is static and can be cached
5. **Error handling**: Handle 404 errors when translations don't exist

## See Also

- [TapSpeak Documentation](TAPSPEAK.md)
- [API Documentation](API.md)
- [Architecture Overview](ARCHITECTURE.md)
