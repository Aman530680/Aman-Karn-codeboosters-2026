# Embeddings & Semantic Search

## Project Objective

This project explores the concepts of **Embeddings** and **Semantic Search** using Sentence Transformers and ChromaDB. It demonstrates how AI can understand the *meaning* behind text — not just keywords — to find the most relevant results.

The project helps to understand:
- What embeddings are and how they represent meaning
- How Sentence Transformers convert text to vectors
- How ChromaDB stores and searches embeddings
- The difference between Keyword Search and Semantic Search
- Cosine similarity for measuring text similarity
- Metadata filtering in vector databases

---

## Technologies Used

- **Python**
- **Sentence Transformers** (`all-MiniLM-L6-v2`)
- **ChromaDB** (Vector Database)
- **NumPy**
- **Pandas**
- **Google Colab**

---

## Project Folder Structure

```text
Day_07_Embeddings_Semantic_Search
│
├── Day_07_Embeddings_SemanticSearch.ipynb
├── Day_07_Embeddings_SemanticSearch!!.ipynb
├── ChromaDB_Semantic_Search.ipynb
├── day_07_embeddings_semanticsearch.py
└── README.md
```

---

## Files Description

### Day_07_Embeddings_SemanticSearch.ipynb
Core notebook covering embeddings concepts — generating sentence embeddings using Sentence Transformers, computing cosine similarity, and performing semantic search manually.

### ChromaDB_Semantic_Search.ipynb
Mini project notebook — Smart Notes Search Engine built using ChromaDB as a vector database. Stores 15 college notes across 3 subjects and performs semantic search with metadata filtering.

### Day_07_Embeddings_SemanticSearch!!.ipynb
Extended version of the embeddings notebook with additional experiments and search comparisons.

### day_07_embeddings_semanticsearch.py
Python script version of the embeddings and semantic search implementation.

---

## Key Concepts Covered

### What are Embeddings?
Embeddings are numerical vector representations of text that capture **semantic meaning**. Similar sentences have vectors that are close together in vector space.

```
"Dog runs fast"   → [0.12, 0.87, 0.34, ...]
"Puppy sprints"   → [0.11, 0.85, 0.36, ...]  ← Similar!
"SQL query runs"  → [0.71, 0.23, 0.91, ...]  ← Different!
```

### Sentence Transformer Model
- **Model Used**: `all-MiniLM-L6-v2`
- **Embedding Dimension**: 384
- **Model Size**: ~90.9 MB
- **Strength**: Fast, efficient, excellent for semantic similarity

### ChromaDB
An open-source vector database that stores embeddings and enables fast semantic search with metadata filtering.

---

## Mini Project: Smart Notes Search Engine

### Dataset
15 college notes across 3 subjects:

| Subject | Notes Count | Topics |
|---------|-------------|--------|
| Machine Learning | 5 | Neural networks, supervised/unsupervised learning, deep learning |
| Programming | 5 | Python, OOP, functions, loops, data structures |
| Database | 5 | SQL, primary keys, normalization, indexes, transactions |

### Notes Stored

**Machine Learning:**
- Neural networks learn patterns from data
- Supervised learning uses labeled examples
- Unsupervised learning finds hidden patterns
- Deep learning powers modern AI systems
- Machine learning improves prediction accuracy

**Programming:**
- Python supports object oriented programming
- Functions help organize code
- Loops automate repetitive tasks
- Lists store multiple values
- Dictionaries store key value pairs

**Database:**
- SQL is used to query databases
- Primary keys uniquely identify records
- Normalization reduces redundancy
- Indexes improve query performance
- Database transactions ensure consistency

---

## Semantic Search Results

### Query: "How do computers learn from examples?"

| Rank | Distance | Result |
|------|----------|--------|
| 1 | 0.9118 | Supervised learning uses labeled examples |
| 2 | 1.0537 | Neural networks learn patterns from data |
| 3 | 1.2088 | Unsupervised learning finds hidden patterns |

> Note: Lower distance = more similar

### Keyword Search vs Semantic Search

**Query**: `"computer learning"`

| Search Type | Result |
|-------------|--------|
| Keyword Search | ❌ No exact matches found |
| Semantic Search | ✅ Found 3 relevant results about ML |

This proves semantic search **understands meaning**, not just exact words.

---

## How to Run the Project

### Step 1: Install Libraries
```python
!pip install chromadb sentence-transformers -q
```

### Step 2: Import Libraries
```python
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
```

### Step 3: Load Embedding Model
```python
model = SentenceTransformer("all-MiniLM-L6-v2")
```

### Step 4: Create ChromaDB Collection
```python
chroma_client = chromadb.Client()

smart_notes = chroma_client.get_or_create_collection(
    name="college_notes"
)
```

### Step 5: Add Notes with Metadata
```python
smart_notes.add(
    documents=notes,
    ids=ids,
    metadatas=metadatas
)
```

### Step 6: Semantic Search
```python
results = smart_notes.query(
    query_texts=["How do computers learn?"],
    n_results=3
)

for doc in results["documents"][0]:
    print(doc)
```

---

## Cosine Similarity Explained

Cosine similarity measures the **angle** between two vectors:
- **Score = 1.0** → Identical meaning
- **Score = 0.0** → Completely unrelated
- **Score = -1.0** → Opposite meaning

```python
from sklearn.metrics.pairwise import cosine_similarity

embedding1 = model.encode(["Machine learning uses data"])
embedding2 = model.encode(["AI learns from examples"])

similarity = cosine_similarity(embedding1, embedding2)
# → High similarity (similar meaning)
```

---

## Keyword Search vs Semantic Search

| Feature | Keyword Search | Semantic Search |
|---------|---------------|-----------------|
| Matching | Exact word match | Meaning-based match |
| Query: "computer learning" | ❌ No results | ✅ Finds ML notes |
| Query: "how to store data" | ❌ No results | ✅ Finds database notes |
| Understanding | None | Full semantic understanding |
| Use Case | Simple filtering | Intelligent retrieval |

---

## ChromaDB Workflow

```
Text Documents
      ↓
Sentence Transformer (all-MiniLM-L6-v2)
      ↓
Embedding Vectors [384 dimensions]
      ↓
ChromaDB Vector Store
      ↓
Query → Embedding → Cosine Distance → Top Results
```

---

## Learning Outcomes

Through this project, we learned:

- **Embeddings**: How text is converted to numerical vectors that capture meaning
- **Sentence Transformers**: Using pre-trained models to generate embeddings
- **ChromaDB**: Creating collections, adding documents, and querying a vector DB
- **Cosine Similarity**: Measuring semantic closeness between embeddings
- **Semantic Search**: Finding relevant content based on meaning, not keywords
- **Metadata Filtering**: Filtering search results by subject/category
- **Keyword vs Semantic**: Understanding the fundamental difference between the two search approaches

---

## Key Results Summary

| Metric | Value |
|--------|-------|
| Total Notes Stored | 15 |
| Subjects Covered | 3 (ML, Programming, Database) |
| Embedding Model | all-MiniLM-L6-v2 |
| Embedding Dimensions | 384 |
| Model Size | ~90.9 MB |
| Search Type | Semantic (meaning-based) |
| Query: "How computers learn?" | Top result: "Supervised learning uses labeled examples" (distance: 0.9118) |

---

## Author

**Aman Karn**

Third Year CSE Student
Sri Eshwar College of Engineering
