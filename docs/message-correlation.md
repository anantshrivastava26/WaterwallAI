# Message Correlation Network

## Overview

The message correlation network creates a graph where **messages are nodes** and **edges represent semantic similarity**. This reveals which messages discuss related topics and how conversations flow across time.

## Architecture

### Embedding Strategy

Uses **deterministic hash-based embeddings**:
- Generates 64-dimensional vectors from message text using SHA256
- Seed-based hashing (64 different hash functions) creates diverse, stable embeddings
- Same message → same embedding (deterministic)
- Fast computation (~67 seconds for 3,246 messages)

### Similarity Computation

- **Metric**: Cosine similarity
- **Threshold**: 0.7 (70% similarity required for edge)
- **Scope**: All-pairs comparison (all messages compared to all others)

## Graph Structure

```
Message 1 (node) ─── 0.82 ──→ Message 42 (similar topic)
                   0.75 ──→ Message 156 (related conversation)
                   0.71 ──→ Message 203 (mentions same person)
```

### Current Statistics
- **Nodes**: 3,246 (messages)
- **Edges**: 426,784 (message correlations)
- **Connectivity**: 8.1% of all possible pairs (426,784 / 5.27M)
- **File size**: 126 MB
- **Build time**: ~67 seconds

## Node Attributes

Each node represents a message:
```json
{
  "id": "msg_123",
  "label": "Anant: Hello, how are you?",
  "file_type": "message",
  "source": "whatsapp",
  "sender": "Anant",
  "timestamp": "2025-06-15T14:30:00",
  "message_preview": "Hello, how are you?",
  "community": 0  // grouped by month
}
```

## Edge Attributes

Each edge represents a semantic correlation:
```json
{
  "source": "msg_123",
  "target": "msg_456",
  "relation": "correlates_with",
  "weight": 0.82,  // cosine similarity
  "confidence_score": 0.82
}
```

## Use Cases

1. **Thread Detection**: Find conversation clusters around topics
   - Messages with high correlation form conversation threads
   
2. **Topic Evolution**: Trace how discussions develop
   - Follow chains of correlated messages across time
   
3. **Conversation Structure**: Understand message flow
   - Identify branching points and merged topics
   
4. **Anomaly Detection**: Find unusual messages
   - Messages with low correlation to others may be off-topic
   
5. **Summary Extraction**: Identify key messages
   - Highly connected nodes are central to conversations

## API Endpoint

### Build Message Correlation Graph
```
POST /graphify/message-correlation
```

**Response:**
```json
{
  "ok": true,
  "nodes": 3246,
  "edges": 426784,
  "graph_file": "data/graphify-data/graphify-out/message-correlation.json",
  "threshold": 0.7,
  "message": "Found 426784 message correlations out of 5266635 possible pairs"
}
```

## Query Examples

### Find all correlations for a specific message
```python
import json

with open('data/graphify-data/graphify-out/message-correlation.json') as f:
    graph = json.load(f)

target_msg_id = "msg_100"

# Find all messages correlated with msg_100
correlated = [
    edge for edge in graph['links'] 
    if edge['source'] == target_msg_id or edge['target'] == target_msg_id
]

# Sort by similarity
correlated.sort(key=lambda x: x['weight'], reverse=True)
for edge in correlated[:5]:
    print(f"Similarity: {edge['weight']:.2f}")
```

### Find conversation clusters
```python
# Messages with high local clustering coefficient form dense conversation threads
# Can use NetworkX to analyze:
import networkx as nx

G = nx.node_link_graph(graph)
# Find communities with high clustering
communities = list(nx.community.greedy_modularity_communities(G))
```

## Performance

- **Build time**: ~67 seconds for 3,246 messages
- **File size**: 126 MB (large due to dense edge list)
- **Query time**: Instant (file-based, no server recompute)

## Comparison with Semantic Graph

| Aspect | Semantic Graph | Message Correlation |
|--------|---|---|
| **Nodes** | 986 entities | 3,246 messages |
| **Edges** | 3,606 relationships | 426,784 correlations |
| **Purpose** | Entity relationships | Message similarity |
| **Use case** | What topics exist? | Which messages relate? |
| **Computation** | spaCy NER | Hash embeddings |

## Future Enhancements

- **Temporal analysis**: Decay edge weights by time distance
- **Sender-based filtering**: Correlations within/across speakers
- **Topic clustering**: Auto-detect conversation topics from dense regions
- **Dynamic visualization**: Interactive exploration with filtering
- **Incremental updates**: Add new messages without full recompute
