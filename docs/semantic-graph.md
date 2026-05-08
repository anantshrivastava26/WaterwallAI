# Semantic Knowledge Graph

## Overview

The system extracts a semantic knowledge graph from ingested messages using spaCy named entity recognition (NER). This graph identifies entities (people, organizations, locations, events, products) and their relationships.

## Architecture

### Pipeline

```
Messages (SQLite)
    ↓
regenerate_inputs(): Dump to markdown per source/month
    ↓
extract_semantic_graph(): spaCy NER extraction
    ↓
graph.json (semantic knowledge graph)
    ↓
graph.html (interactive visualization)
```

### Automatic Updates

When new messages are ingested via `/ingest/whatsapp`:
1. Messages are stored in SQLite
2. If `inserted > 0`, `refresh_graph()` is triggered as a background task
3. Graph rebuilds automatically with new entities and relationships

### Entity Types

Extracted entities (spaCy categories):
- **PERSON**: People names
- **ORG**: Organizations
- **GPE**: Geopolitical entities (countries, cities)
- **EVENT**: Events
- **PRODUCT**: Products

### Relationships

The graph captures:
1. **Co-mentions**: Entities mentioned together in the same message
   - Weight: `min(occurrence_count / 10, 1.0)` (max 1.0)
2. **Temporal associations**: Entity mentions in specific time periods
   - Weight: 1.0 (presence in a month)

## Files

- `backend/app/services/semantic_extractor.py` - Entity extraction using spaCy
- `backend/app/services/graphify_export.py` - Orchestration (inputs dump + extraction)
- `data/graphify-data/` - Raw markdown dumps (gitignored)
- `data/graphify-data/graphify-out/` - Output graph (gitignored)
  - `graph.json` - Full semantic graph in NetworkX format
  - `graph.html` - Interactive D3 visualization
  - `graph.json` contains nodes with attributes and edges with relation types

## Current Statistics

- **Total messages**: 3,246 (as of latest ingestion)
- **Entities extracted**: 986 nodes
- **Relationships**: 3,606 edges
- **Time span**: June 2025 - May 2026

## API Endpoints

### Ingest WhatsApp Chat
```
POST /ingest/whatsapp
```
- Uploads .txt WhatsApp export
- Auto-triggers graph refresh if new messages inserted
- Returns: `{inserted: N, skipped: M}`

### Refresh Graph (Manual)
```
POST /graphify/refresh
```
- Regenerates inputs (markdown dumps)
- Extracts semantic graph
- Returns: `{inputs: {...}, extract: {...}}`

## Local Development

### View the Graph

1. Open `data/graphify-data/graphify-out/graph.html` in a browser
2. Interactive D3 visualization with:
   - Node colors by entity type
   - Edge weights as relationship strength
   - Hover for details, click to focus

### Query the Graph

```python
import json
with open('data/graphify-data/graphify-out/graph.json') as f:
    graph = json.load(f)

# Find all PERSON entities
people = [n for n in graph['nodes'] if n.get('entity_type') == 'PERSON']

# Find entities connected to a specific node
def neighbors(node_id):
    edges = [e for e in graph['links'] if e['source'] == node_id or e['target'] == node_id]
    return edges
```

## Performance

- spaCy processing: ~4-5 seconds for 3,246 messages
- No external API calls required (fully local)
- Graph size: ~1.4 MB for ~1000 nodes and ~3600 edges

## Privacy

- All graph data stored in `data/graphify-data/` (gitignored)
- No data sent to external services
- Fully private knowledge graph

## Future Enhancements

Possible improvements:
- Filter low-confidence entities (noise reduction)
- Extract additional relationships (verb-based patterns)
- Implement entity linking (resolve "Apple Inc." ≠ "apple fruit")
- Export to Neo4j for more sophisticated querying
- Build PERSON ↔ ORGANIZATION relationships from message context
