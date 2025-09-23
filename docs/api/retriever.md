# Retriever API Reference

## Overview

The Retriever module provides semantic search capabilities using FAISS (Facebook AI Similarity Search) for enhanced information retrieval.

## Class: Retriever

```python
from sigma_nex.core.retriever import Retriever

retriever = Retriever(config)
```

### Constructor

**Parameters:**
- `config` (dict): Configuration containing retrieval settings

### Methods

#### `retrieve(query: str, top_k: int = 5) -> List[str]`

Retrieve most relevant documents for a given query.

**Parameters:**
- `query` (str): Search query
- `top_k` (int): Number of top results to return (default: 5)

**Returns:**
- `List[str]`: List of relevant document texts

**Example:**
```python
retriever = Retriever(config)
docs = retriever.retrieve("primo soccorso ferita", top_k=3)
for doc in docs:
    print(doc)
```

#### `add_document(text: str, metadata: dict = None)`

Add a new document to the search index.

**Parameters:**
- `text` (str): Document content
- `metadata` (dict, optional): Additional document metadata

#### `build_index(documents: List[str])`

Build or rebuild the FAISS search index.

**Parameters:**
- `documents` (List[str]): List of documents to index

#### `save_index(path: str)`

Save the current index to disk.

**Parameters:**
- `path` (str): File path to save the index

#### `load_index(path: str)`

Load an existing index from disk.

**Parameters:**
- `path` (str): File path to load the index from

## FAISS Integration

### Index Types

SIGMA-NEX supports multiple FAISS index types:

```python
# Flat L2 index (exact search)
index_flat = faiss.IndexFlatL2(dimension)

# IVF index (approximate search, faster)
nlist = 100
quantizer = faiss.IndexFlatL2(dimension)
index_ivf = faiss.IndexIVFFlat(quantizer, dimension, nlist)

# HNSW index (hierarchical navigable small world)
index_hnsw = faiss.IndexHNSWFlat(dimension, M=16)
```

### Embedding Models

Default embedding pipeline:
- **Sentence Transformers**: `all-MiniLM-L6-v2`
- **Multilingual Support**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Medical Specialized**: `clinical-bert-embeddings`

```python
from sentence_transformers import SentenceTransformer

# Default model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Medical model (if available)
medical_model = SentenceTransformer('clinical-bert-embeddings')
```

## Configuration

```yaml
retrieval:
  enabled: true                    # Enable retrieval system
  index_type: "flat"              # Index type: flat, ivf, hnsw
  top_k: 5                        # Default number of results
  similarity_threshold: 0.7       # Minimum similarity score
  
embedding:
  model_name: "all-MiniLM-L6-v2"  # Embedding model
  dimension: 384                   # Embedding dimension
  batch_size: 32                  # Encoding batch size
  
faiss:
  index_path: "data/moduli.index" # Index file path
  mapping_path: "data/moduli.mapping.json"  # Document mapping
  nlist: 100                      # IVF parameter
  nprobe: 10                      # Search parameter
```

## Document Processing

### Text Preprocessing

```python
def preprocess_text(text: str) -> str:
    """Preprocess text for optimal retrieval."""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters (keep medical symbols)
    text = re.sub(r'[^\w\s\.,!?;:()\-°%]', '', text)
    
    # Normalize medical terms
    text = normalize_medical_terms(text)
    
    return text
```

### Chunking Strategy

```python
def chunk_document(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Split document into overlapping chunks."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Find natural break point
        if end < len(text):
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            
            if break_point > start + chunk_size // 2:
                end = break_point + 1
                chunk = text[start:end]
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return chunks
```

## Search Strategies

### Semantic Search

```python
def semantic_search(query: str, top_k: int = 5) -> List[Dict]:
    """Perform semantic similarity search."""
    # Encode query
    query_embedding = model.encode([query])
    
    # Search index
    scores, indices = index.search(query_embedding, top_k)
    
    # Format results
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if score >= similarity_threshold:
            results.append({
                'text': documents[idx],
                'score': float(score),
                'index': int(idx)
            })
    
    return results
```

### Hybrid Search

```python
def hybrid_search(query: str, top_k: int = 5) -> List[str]:
    """Combine semantic and keyword search."""
    # Semantic search results
    semantic_results = semantic_search(query, top_k * 2)
    
    # Keyword search results
    keyword_results = keyword_search(query, top_k * 2)
    
    # Merge and re-rank results
    combined = merge_results(semantic_results, keyword_results)
    return rerank_results(combined, query)[:top_k]
```

### Medical Search Enhancement

```python
def medical_search(query: str, top_k: int = 5) -> List[str]:
    """Enhanced search for medical queries."""
    # Extract medical entities
    medical_entities = extract_medical_entities(query)
    
    # Expand query with medical synonyms
    expanded_query = expand_medical_query(query, medical_entities)
    
    # Weighted search (medical content prioritized)
    results = weighted_search(expanded_query, weights={
        'emergency': 2.0,
        'medical': 1.5,
        'general': 1.0
    })
    
    return results[:top_k]
```

## Performance Optimization

### Index Optimization

```python
# Train IVF index for better performance
if index_type == "ivf":
    training_data = sample_embeddings(10000)  # Sample for training
    index.train(training_data)
    
# Set search parameters
index.nprobe = 10  # Number of clusters to search
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_retrieve(query: str, top_k: int = 5) -> tuple:
    """Cache frequent queries."""
    results = retriever.retrieve(query, top_k)
    return tuple(results)  # Convert to hashable type for caching
```

### Batch Processing

```python
def batch_retrieve(queries: List[str], top_k: int = 5) -> List[List[str]]:
    """Process multiple queries efficiently."""
    # Encode all queries at once
    query_embeddings = model.encode(queries)
    
    # Batch search
    all_scores, all_indices = index.search(query_embeddings, top_k)
    
    # Format results
    results = []
    for scores, indices in zip(all_scores, all_indices):
        query_results = [documents[idx] for idx in indices 
                        if scores[i] >= similarity_threshold]
        results.append(query_results)
    
    return results
```

## Integration Examples

### With Context Builder

```python
def enhanced_context_building(query: str, history: List[str]) -> str:
    """Build context enhanced with retrieval."""
    # Retrieve relevant documents
    relevant_docs = retriever.retrieve(query, top_k=3)
    
    # Build base context
    base_context = context_builder.build_prompt(query, history)
    
    # Add retrieved information
    if relevant_docs:
        context_enhancement = "\n\nINFORMAZIONI RILEVANTI:\n"
        for i, doc in enumerate(relevant_docs, 1):
            context_enhancement += f"{i}. {doc}\n\n"
        
        base_context += context_enhancement
    
    return base_context
```

### Medical Emergency Mode

```python
def emergency_retrieval(query: str) -> List[str]:
    """Priority retrieval for medical emergencies."""
    # Detect emergency keywords
    emergency_terms = ['emergenza', 'urgente', 'sangue', 'dolore', 'shock']
    is_emergency = any(term in query.lower() for term in emergency_terms)
    
    if is_emergency:
        # Search emergency protocols first
        emergency_docs = retriever.retrieve(
            f"emergenza primo soccorso {query}", 
            top_k=3
        )
        
        # Add general medical info
        general_docs = retriever.retrieve(query, top_k=2)
        
        return emergency_docs + general_docs
    
    return retriever.retrieve(query, top_k=5)
```