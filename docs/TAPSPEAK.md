# TapSpeak Translation System

**TapSpeak is a bi-directional translation engine** that converts complex biotech/networkology concepts into **instantly memorable plain English** using basketball analogies while maintaining precise operational mappings.

## Philosophy

> **"Common man must grok rocket science in 5 seconds"**

TapSpeak is not just simplification—it's a **cognitive compression algorithm** for mass adoption of high science.

## 7-Layer Translation Structure

Every TapSpeak translation follows this format:

```
┌──────────────────────────────────────────────────────────────┐
│ 1. TapSpeak        │ Memorable plain English hook             │
├──────────────────────────────────────────────────────────────┤
│ 2. Professional    │ Technical term or metric                 │
├──────────────────────────────────────────────────────────────┤
│ 3. Operational     │ How it works mechanistically             │
├──────────────────────────────────────────────────────────────┤
│ 4. Translational   │ Real-world impact for common man         │
├──────────────────────────────────────────────────────────────┤
│ 5. Confidence      │ ESAT/CEP validation scores               │
├──────────────────────────────────────────────────────────────┤
│ 6. Hooks           │ Mnemonic device for memory               │
├──────────────────────────────────────────────────────────────┤
│ 7. Tags            │ Searchable categories                    │
└──────────────────────────────────────────────────────────────┘
```

## Example Translation

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

## Confidence Metrics

TapSpeak uses two validation scores:

- **ESAT (Everyday Speech Accuracy Threshold)**: 0-100 score measuring how well common people understand the translation
  - **Minimum**: 70% (70.0)
  - **Target**: 85%+

- **CEP (Conceptual Equivalence Precision)**: 0-100 score measuring how well the translation preserves technical meaning
  - **Minimum**: 80% (80.0)
  - **Target**: 90%+

A translation is considered valid when: `ESAT ≥ 70 AND CEP ≥ 80`

## BBTech Translation Layer (Basketball → Biology)

TapSpeak uses NBA stats as universal biotech metrics:

| Basketball Stat | Biotech Analog | Networkology Meaning |
|----------------|----------------|---------------------|
| **3PAr** (3-point attempt rate) | Innovation Exploration | Mutation spread rate |
| **TOV** (Turnovers) | Error Propagation | Eigen error threshold |
| **Gravity** | Hub Attractiveness | Scale-free centrality |
| **Net Rating** | Pathway Contribution | Causal driver score |
| **WPA Clutch** | Rare-Event Reliability | Stress viability index |

### Why Basketball?

1. **Universally understood**: NBA is globally recognized
2. **Dual coding**: Visual (sports) + Verbal (hooks) = 6x retention
3. **Emotional**: Sports passion → biotech excitement
4. **Quantified**: Stats are precise and measurable

## API Endpoints

### Get All Concepts

```bash
GET /api/v1/tapspeak/concepts?category=core_concepts
```

**Categories**:
- `core_concepts` - Core biotech + networkology concepts (5 translations)
- `networkology_workflow` - Workflow steps (5 translations)
- `codex_translations` - Codex metrics (3 translations)

**Response**:
```json
[
  {
    "id": 1,
    "tap_speak": "Cells talk in 3D neighborhoods",
    "professional": "Spatial transcriptomics + tissue geometry",
    ...
  }
]
```

### Get BBTech Mappings

```bash
GET /api/v1/tapspeak/bbtech
```

Returns all Basketball-Biotech bridge mappings.

### Search Translations

```bash
POST /api/v1/tapspeak/search
Content-Type: application/json

{
  "query": "hub",
  "tags": ["gravity", "hubs"],
  "min_esat": 70.0,
  "min_cep": 80.0
}
```

**Search by**:
- Query text (searches tap_speak, professional, hooks, tags)
- Tags (filter by specific tags)
- Category (filter by category)
- Confidence thresholds

### Translate Technical Term

```bash
POST /api/v1/tapspeak/translate
Content-Type: application/json

{
  "technical_term": "Hub centrality",
  "domain": "biotech"
}
```

**Response**:
```json
{
  "id": 5,
  "tap_speak": "Big dogs eat first (high Gravity)",
  "professional": "Hub centrality + attractiveness index",
  ...
}
```

### Get Dashboard Data

```bash
GET /api/v1/tapspeak/dashboard
```

Returns complete TapSpeak dashboard with all concepts, workflows, metrics, and BBTech mappings.

### Get Statistics

```bash
GET /api/v1/tapspeak/stats
```

Returns translation statistics:
```json
{
  "total_translations": 13,
  "average_confidence": {
    "esat": 82.3,
    "cep": 87.3
  },
  "by_category": {
    "core_concepts": 5,
    "networkology_workflow": 5,
    "codex_translations": 3,
    "bbtech_mappings": 3
  }
}
```

## Core Concepts (5)

### 1. Cells talk in 3D neighborhoods
- **Professional**: Spatial transcriptomics + tissue geometry
- **Operational**: MERFISH maps RNA locations in tissue slices
- **Translational**: Same mutation hits heart brain toe differently due to location
- **Hook**: Cells have addresses not just phone numbers

### 2. Fat storing switch flips everywhere
- **Professional**: Pan-cellular network dysfunction
- **Operational**: MC4R mutation disrupts leptin signaling across all cells
- **Translational**: One gene fix cures obesity in heart brain liver simultaneously
- **Hook**: Same broken wire different room symptoms

### 3. Cut the fat (3PAr high)
- **Professional**: Innovation exploration metric
- **Operational**: High 3-point attempt rate = adaptation cycle spread
- **Translational**: Biotech pathways that explore more options win evolution
- **Hook**: Curry contagion - spread good ideas fast

### 4. Don't drop the ball (low TOV)
- **Professional**: Error propagation threshold
- **Operational**: Turnover minimization prevents network collapse
- **Translational**: Too many mutations = system crashes like Eigen threshold
- **Hook**: One fumble loses the game

### 5. Big dogs eat first (high Gravity)
- **Professional**: Hub centrality + attractiveness index
- **Operational**: Scale-free network hubs control 80% system state
- **Translational**: Fix the kingpin one shot cures whole disease
- **Hook**: Elephant in room pulls whole circus

## Networkology Workflow (5 Steps)

### 10. Suck in all the data
- **Professional**: Heterogeneous federation (BioKleisli)
- **Operational**: OMIM + GenBank + KEGG + MERFISH via middleware
- **Hook**: Vacuum cleaner for science papers

### 11. Draw the wiring diagram
- **Professional**: Geometric interactome construction
- **Operational**: Neo4j + SpatialGCN builds 3D manifold
- **Hook**: City map not phone book

### 12. Find the broken wires
- **Professional**: Causal discovery + hub detection
- **Operational**: PC algorithm + NOTEARS on geometric gradients
- **Hook**: Detective finds smoking gun

### 13. Score the fixes
- **Professional**: Codex metrics overlay
- **Operational**: Trueness(Flow+Gravity) ranks CRISPR targets
- **Hook**: NBA stats for DNA repairs

### 14. Build the repair crew
- **Professional**: Vector engineering + digital twins
- **Operational**: AAV9 follows tissue curvature to hubs
- **Hook**: Uber for CRISPR delivery

## Codex Translations (3 Metrics)

### 20. True as steel
- **Professional**: Trueness metric
- **Operational**: CRISPR edit fidelity 1-hamming_distance
- **Hook**: No typos in the genome edit

### 21. Traffic flow smooth
- **Professional**: Flow metric
- **Operational**: AAV delivery efficiency x half_life
- **Hook**: FedEx for genes

### 22. Kingpin power
- **Professional**: Gravity metric
- **Operational**: log(degree) x eigenvector_centrality
- **Hook**: Pull one thread unravel disease

## Usage Examples

### Python Client

```python
import requests

# Get all core concepts
response = requests.get('http://localhost:8000/api/v1/tapspeak/concepts?category=core_concepts')
concepts = response.json()

for concept in concepts:
    print(f"{concept['tap_speak']} → {concept['professional']}")

# Search for hub-related translations
search_response = requests.post('http://localhost:8000/api/v1/tapspeak/search', json={
    "query": "hub",
    "min_esat": 85.0
})
results = search_response.json()

# Translate a technical term
translate_response = requests.post('http://localhost:8000/api/v1/tapspeak/translate', json={
    "technical_term": "CRISPR-Cas9",
    "domain": "biotech"
})
translation = translate_response.json()
print(f"TapSpeak: {translation['tap_speak']}")
```

### JavaScript/TypeScript Client

```typescript
// Get dashboard data
const response = await fetch('http://localhost:8000/api/v1/tapspeak/dashboard');
const dashboard = await response.json();

console.log(`Total translations: ${dashboard.total_translations}`);
console.log(`Average ESAT: ${dashboard.average_confidence.esat}`);

// Search with tags
const searchResponse = await fetch('http://localhost:8000/api/v1/tapspeak/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    tags: ['gravity', 'hubs'],
    min_esat: 80.0,
    min_cep: 85.0
  })
});

const results = await searchResponse.json();
```

## Integration with NetworkCellularMap

TapSpeak integrates seamlessly with the existing NetworkCellularMap v2.0 platform:

1. **Networkologist Diagnose** - Display TapSpeak translations alongside technical diagnosis
2. **Universal Hub Analysis** - Show BBTech analogies for hub metrics
3. **Codex Metrics** - Use TapSpeak hooks in metric displays
4. **Repair Design** - Explain CRISPR strategies in plain English

## Why TapSpeak Works (Cognitive Science)

1. **Dual Coding Theory**: Visual (NBA) + Verbal (hooks) = 6x better retention
2. **Chunking**: Complex concepts → 3-word phrase = bypasses working memory limits
3. **Emotional Connection**: Sports passion transfers to biotech excitement
4. **Social Proof**: "Even grandma gets it" → cascading trust

## Future Enhancements

- **LLM Integration**: Fine-tune spaCy + GPT for automatic TapSpeak generation
- **Overlay365 Gamification**: Quests for translating biotech papers
- **Viral Challenges**: "Farmers explain CRISPR" video campaigns
- **Meme Generation**: Automatic hook → meme pipeline
- **Real-time Translation**: Live TapSpeak overlay on research papers

## Tags Reference

Available tags for filtering:
- `geometry`, `spatial`, `merfish`, `networkology`
- `pan_cellular`, `hubs`, `obesity`, `causal`
- `basketball`, `biotech`, `gravity`, `innovation`
- `error_threshold`, `stability`, `replicator`
- `achilles`, `codex`
- `ingest`, `federation`, `biokleisli`
- `mapping`, `manifold`
- `ai`
- `gamification`, `trueness`
- `intervention`, `crispr`, `digital_twin`
- `flow`, `viral_vector`
- `bbtech`, `3par`, `evolution`
- `tov`, `eigen_threshold`
- `scale_free`

## License

Part of NetworkCellularMap v2.0 - See LICENSE file
