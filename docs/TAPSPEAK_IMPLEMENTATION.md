# TapSpeak Technical Reference

## Overview

TapSpeak is a bi-directional translation engine that converts complex biotech/networkology concepts into instantly memorable plain English using basketball analogies.

## Architecture

### Backend Components

**Translation Engine** (`backend/app/services/tapspeak.py`)
- 13 curated translations across domains
- 7-layer translation structure
- Tag-based search with deduplication
- Public API methods for concept retrieval

**API Endpoints** (`backend/app/api/endpoints/tapspeak.py`)
- 9 REST endpoints for translation services
- Category-based filtering
- Search and validation capabilities

**Data Models** (`backend/app/models/schemas.py`)
- `TapSpeakTranslation`: Core translation schema
- `BBTechMapping`: Basketball-to-biotech bridge
- `ConfidenceMetrics`: ESAT/CEP validation

### Frontend Components

**UI Components**
- `TapSpeakCard.tsx`: Individual translation display with view toggle
- `TapSpeakDashboard.tsx`: Complete dashboard with search and filters

**API Integration**
- `tapspeak-api.ts`: Type-safe API client
- `tapspeak-types.ts`: Shared TypeScript interfaces

### Translation Catalog

**Available Translations**: 13 translations
- 5 Core biotech/networkology concepts
- 5 Networkology workflow steps
- 3 Codex metrics
- 3 BBTech bridge mappings

**Searchable Tags**: 30 unique tags for filtering

## Features

### Core Translation Engine
- 7-layer translation structure (TapSpeak → Professional → Operational → Translational → Confidence → Hooks → Tags)
- Confidence metrics (ESAT/CEP) with validation thresholds
- Tag-based search and filtering
- Technical term translation
- Translation quality validation
- BBTech bridge (Basketball stats → Biotech metrics)

### API Endpoints
- `GET /api/v1/tapspeak/concepts` - Get all concepts with optional category filter
- `GET /api/v1/tapspeak/bbtech` - Get BBTech mappings
- `POST /api/v1/tapspeak/search` - Search with query, tags, confidence filters
- `POST /api/v1/tapspeak/translate` - Translate technical term
- `POST /api/v1/tapspeak/validate` - Validate translation quality
- `GET /api/v1/tapspeak/dashboard` - Get complete dashboard data
- `GET /api/v1/tapspeak/stats` - Get statistics
- `GET /api/v1/tapspeak/concept/{id}` - Get specific concept
- `GET /api/v1/tapspeak/tags` - Get all available tags

### Frontend Components
- TapSpeakCard with common/expert view toggle
- TapSpeakDashboard with full search and filtering
- TypeScript API client
- Shared type definitions
- Confidence visualization with progress bars
- Tag filtering UI
- Category tabs
- Responsive design

## Translation Quality Standards

### Confidence Metrics
- **ESAT (Everyday Speech Accuracy Threshold)**: Measures comprehension by non-experts (minimum 70%)
- **CEP (Conceptual Equivalence Precision)**: Measures technical accuracy (minimum 80%)

All translations must meet both minimum thresholds to be considered valid.

## Example Translations

### Core Concept
```
TapSpeak: "Big dogs eat first (high Gravity)"
Professional: "Hub centrality + attractiveness index"
Operational: "Scale-free network hubs control 80% system state"
Translational: "Fix the kingpin one shot cures whole disease"
Hook: "Elephant in room pulls whole circus"
Confidence: ESAT=90%, CEP=95%
Tags: hubs, achilles, gravity, codex
```

### BBTech Mapping
```
TapSpeak: "Curry contagion"
Professional: "3PAr = innovation exploration"
Operational: "High 3PT% = adaptation cycle spread"
Translational: "Biotech needs bold experiments like Steph shots"
Hook: "Splash brothers = mutation winners"
Confidence: ESAT=75%, CEP=80%
Tags: bbtech, 3par, evolution
```

## Integration Points

### With Existing NetworkCellularMap Features

1. **Networkologist Diagnose**: Add TapSpeak explanations to diagnosis results
2. **Universal Hub Analysis**: Translate hub metrics to plain English
3. **Codex Metrics**: Trueness, Flow, Gravity have TapSpeak translations
4. **Repair Design**: Explain CRISPR strategies using basketball analogies

## Usage Examples

### Python
```python
from app.services.tapspeak import get_tapspeak_engine

engine = get_tapspeak_engine()
translation = engine.translate_term("Hub centrality")
print(f"{translation.tap_speak} → {translation.hooks}")
```

### TypeScript
```typescript
import { tapspeakAPI } from '@/lib/tapspeak-api';

const translation = await tapspeakAPI.translateTerm({
  technical_term: 'Hub centrality'
});
```

### cURL
```bash
curl -X POST http://localhost:8000/api/v1/tapspeak/translate \
  -H "Content-Type: application/json" \
  -d '{"technical_term": "Hub centrality"}'
```

## Documentation

Additional documentation available:
- **TAPSPEAK.md**: Full guide with philosophy, structure, and complete translation catalog
- **TAPSPEAK_EXAMPLES.md**: Detailed code samples for Python, TypeScript, and cURL
- **README.md**: Integration with NetworkCellularMap platform

## Future Enhancements

Potential extensions for the TapSpeak system:
- LLM integration for automatic TapSpeak generation
- User-submitted translations with community validation
- Translation voting/rating system
- Multi-language support
- Audio pronunciation of TapSpeak phrases
- Gamification integration with Overlay365
- Meme generation from hooks
