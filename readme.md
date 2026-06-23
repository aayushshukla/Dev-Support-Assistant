# 🚀 Developer Support Assistant

> An Enterprise-Grade Multi-Agent Retrieval-Augmented Generation (RAG) platform for software engineering knowledge retrieval, troubleshooting, and documentation assistance.

---

# 📖 Overview

Developer Support Assistant is an AI-powered multi-agent system designed to help developers quickly retrieve and understand technical knowledge scattered across APIs, documentation, runbooks, architecture documents, and source code.

The platform leverages **Large Language Models (LLMs)**, **Retrieval-Augmented Generation (RAG)**, **semantic search**, and **specialized AI agents** to provide context-aware, accurate, and explainable answers.

The system is built to simulate a real-world enterprise developer support ecosystem.

---

# ✨ Key Features

## 🤖 Multi-Agent Architecture

The platform consists of specialized agents orchestrated by a Supervisor Agent.

- Supervisor Agent
- Query Router Agent
- API Specialist Agent
- Runbook Agent
- Documentation Agent
- Code Documentation Agent

---

## 🔍 Retrieval-Augmented Generation (RAG)

- Semantic Chunking
- Embedding Generation
- Vector Similarity Search
- Context Retrieval
- LLM Response Generation

---

## 📚 Document Ingestion

Supported document formats:

- CSV
- PDF
- Markdown
- TXT
- JSON

Features:

- Automatic metadata extraction
- Hybrid chunking strategy
- Batch ingestion
- Duplicate detection

---

## 🧠 Semantic Search

Uses:

- PGVector
- Cosine Similarity
- Domain-aware retrieval
- Metadata filtering

Supported domains:

- Spring Boot
- FastAPI
- Django
- Docker
- Kubernetes
- PostgreSQL
- React
- Java
- Python
- DevOps

---

## 🌐 Intelligent Web Fallback

When the internal knowledge base cannot answer a query confidently, the system automatically falls back to web search.

Benefits:

- Reduces hallucination
- Improves answer coverage
- Supports unseen topics
- Enhances user experience

Workflow:

```text
User Query
     │
     ▼
Vector Search
     │
     ├── Relevant Context Found
     │            │
     │            ▼
     │      Generate Answer
     │
     └── No Relevant Context
                  │
                  ▼
           Web Fallback Search
                  │
                  ▼
            Generate Answer
```

---

# 🏗️ System Architecture

```text
+------------------------------------------------------------+
|                    Streamlit Frontend                      |
+----------------------------+-------------------------------+
                             |
                             ▼
+------------------------------------------------------------+
|                       FastAPI Backend                      |
+----------------------------+-------------------------------+
                             |
                             ▼
+------------------------------------------------------------+
|                    Supervisor Agent                        |
+----------------------------+-------------------------------+
                             |
                             ▼
+------------------------------------------------------------+
|                     Query Router Agent                     |
+------------+----------------+----------------+-------------+
             |                |                |
             ▼                ▼                ▼
+----------------+ +----------------+ +---------------------+
| API Agent      | | Runbook Agent | | Documentation Agent |
+----------------+ +----------------+ +---------------------+
             |
             ▼
+------------------------------------------------------------+
|                  Retrieval Layer                           |
|         Vector Search + Metadata Filtering                |
+------------------------------------------------------------+
                             |
                             ▼
+------------------------------------------------------------+
|                 PostgreSQL + PGVector                     |
+------------------------------------------------------------+
                             |
                             ▼
+------------------------------------------------------------+
|                   External Web Search                     |
+------------------------------------------------------------+
```

---

# 🧩 Project Structure

```text
dev-support/
│
├── app.py
│
├── backend/
│
│   ├── agents/
│   │     ├── supervisor.py
│   │     ├── router.py
│   │     ├── api_agent.py
│   │     ├── runbookagent.py
│   │     ├── documentagent.py
│   │     └── codedocumentationagent.py
│   │
│   ├── api/
│   ├── chunking/
│   ├── embeddings/
│   ├── generation/
│   ├── ingestion/
│   ├── retrieval/
│   ├── dbops/
│   ├── services/
│   └── models/
│
├── frontend/
├── styles/
├── data/
├── uploads/
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

## Frontend

- Streamlit
- HTML
- CSS

## Backend

- FastAPI
- Python 3.11+

## AI Frameworks

- LangChain
- Sentence Transformers
- OpenAI API

## Vector Database

- PostgreSQL
- PGVector

## Embedding Model

```text
BAAI/bge-base-en-v1.5
```

## Evaluation

- RAGAS
- Custom Agent Metrics

## Containerization

- Docker
- Docker Compose

---

# 🔄 RAG Pipeline

## Indexing Phase

```text
Documents
    │
    ▼
Document Loader
    │
    ▼
Hybrid Chunking
    │
    ▼
Embedding Generation
    │
    ▼
PGVector Storage
```

---

## Retrieval Phase

```text
User Query
    │
    ▼
Query Embedding
    │
    ▼
Vector Search
    │
    ▼
Metadata Filtering
    │
    ▼
Top-K Retrieval
    │
    ▼
Context Building
```

---

## Generation Phase

```text
Question + Retrieved Context
              │
              ▼
             LLM
              │
              ▼
       Final Response
```

---

# ✂️ Hybrid Chunking Strategy

The system uses a two-stage chunking strategy.

## Stage 1: Structure-Aware Chunking

Uses:

```python
MarkdownHeaderTextSplitter
```

Benefits:

- Preserves document hierarchy
- Maintains section boundaries

---

## Stage 2: Semantic Chunking

Uses:

```python
SemanticChunker
```

Benefits:

- Produces semantically meaningful chunks
- Improves retrieval quality

---

# 📊 Evaluation Metrics

## RAG Evaluation (RAGAS)

The system evaluates generated responses using:

- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall

---

## Agent Evaluation

Tracks:

| Metric              | Description                   |
| ------------------- | ----------------------------- |
| Routing Accuracy    | Correct agent selection       |
| Retrieval Latency   | Vector search time            |
| LLM Latency         | Response generation time      |
| Total Response Time | End-to-end latency            |
| Agent Usage         | Frequency of agent invocation |

---

# 📈 Statistics Dashboard

The Streamlit dashboard provides:

- Total Documents
- Total Chunks
- Total Domains
- Average Retrieval Time
- Agent Usage Statistics
- Query Metrics
- Upload Statistics

---

# 🚀 Installation

## Clone Repository

```bash
git clone <repository-url>

cd dev-support
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🐳 Database Setup

## Docker Compose

```yaml
version: "3.9"

services:
  pgvector-db:
    image: pgvector/pgvector:pg17

    container_name: pgvector-db

    restart: always

    environment:
      POSTGRES_DB: developer_assistant
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

    ports:
      - "5432:5432"

    volumes:
      - pgvector_data:/var/lib/postgresql/data

volumes:
  pgvector_data:
```

Start:

```bash
docker compose up -d
```

---

# ▶️ Running the Application

## Backend

```bash
uvicorn backend.api.main:app --reload
```

API Docs:

```text
http://localhost:8000/docs
```

---

## Frontend

```bash
streamlit run app.py
```

Application:

```text
http://localhost:8501
```

---

# 📡 API Endpoints

| Endpoint | Method | Description                |
| -------- | ------ | -------------------------- |
| /ask     | POST   | Ask questions              |
| /upload  | POST   | Upload documents           |
| /stats   | GET    | Fetch dashboard statistics |
| /health  | GET    | Service health check       |

---

# 🔮 Future Enhancements

- Hybrid Retrieval (BM25 + Dense Retrieval)
- Cross Encoder Re-ranking
- Conversation Memory
- Fine-tuning
- Authentication & Authorization
- Observability Dashboard
- Feedback Loop
- Multi-modal Support
