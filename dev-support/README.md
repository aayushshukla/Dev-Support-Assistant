# 🚀 Developer Support Assistant

> An Enterprise-Grade Multi-Agent Retrieval-Augmented Generation (RAG) platform for software engineering knowledge retrieval, troubleshooting, and documentation assistance.

---

## 📖 Overview

Developer Support Assistant is an AI-powered multi-agent system that helps developers quickly retrieve and understand technical knowledge scattered across APIs, documentation, runbooks, architecture documents, and source code.

It combines **hybrid retrieval** (dense vector search + BM25), **cross-encoder re-ranking**, **conversation memory**, and **specialized AI agents** to deliver context-aware, grounded, and explainable answers.

---

## ✨ Key Features

- **Multi-Agent Architecture** — a Supervisor routes each query to a specialized agent (API, Runbook, Code, or Document).
- **Hybrid Retrieval** — dense embeddings and BM25 keyword search fused with Reciprocal Rank Fusion (RRF).
- **Cross-Encoder Re-ranking** — `ms-marco-MiniLM-L-6-v2` re-scores candidates for high precision.
- **Conversation Memory** — follow-up questions like *"how to stop it"* resolve against previous turns.
- **Document Ingestion** — CSV, PDF, and Markdown with automatic chunking, embedding, and duplicate detection.
- **Web Fallback** — Serper-powered external search when the internal knowledge base can't answer confidently.
- **Analytics Dashboard** — live stats on documents, chunks, agent usage, cache, and feedback.
- **RAGAS Evaluation** — automated benchmarking on Faithfulness, Answer Relevancy, Context Precision, and Context Recall.

---

## 🏗️ System Architecture

```text
              Streamlit Frontend
                      │
                      ▼
               FastAPI Backend
                      │
                      ▼
              Supervisor Agent
                      │
                      ▼
              Query Router Agent
        ┌─────────────┼─────────────┬──────────────┐
        ▼             ▼             ▼              ▼
   API Agent    Runbook Agent   Code Agent   Document Agent
        └─────────────┴─────────────┴──────────────┘
                      │
                      ▼
        Hybrid Retrieval (Dense + BM25 + RRF)
                      │
                      ▼
          Cross-Encoder Re-ranking
                      │
                      ▼
            PostgreSQL + pgvector
                      │
                      ▼
          External Web Search (fallback)
```

---

## 🔄 RAG Pipeline

**Indexing:** Documents → Loader → Recursive Chunking (1000 / 200 overlap) → Embedding → pgvector storage

**Retrieval:** Query → Dense search (top-20) + BM25 (top-20) → RRF fusion → Cross-encoder re-rank → Top-k context

**Generation:** Query + Context + Chat history → GPT-4o-mini → Grounded answer

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI (Python 3.11+) |
| Vector store | PostgreSQL + pgvector |
| Embeddings | OpenAI `text-embedding-3-small` |
| Retrieval | Dense + BM25 + Reciprocal Rank Fusion |
| Re-ranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| Generation | GPT-4o-mini |
| Evaluation | RAGAS |
| Containerization | Docker, Docker Compose |

---

## 📊 Evaluation Results (RAGAS)

Averaged over an 18-question benchmark across Docker, Kubernetes, Jenkins, and FastAPI:

| Metric | Score |
|--------|-------|
| Faithfulness | 0.87 |
| Answer Relevancy | 0.66 |
| Context Precision | 1.00 |
| Context Recall | 1.00 |

Alongside RAGAS, the dashboard tracks **operational metrics**: routing distribution per agent, retrieval and LLM latency, total response time, cache hit ratio, and positive/negative feedback counts.

---

## 🧩 Project Structure

```text
dev-support/
├── app.py                         # Streamlit entry point
├── docker-compose.yml             # pgvector database
├── backend/
│   ├── agents/                    # supervisor, router, api/runbook/code/document agents
│   ├── api/                       # FastAPI routes (ask, upload, stats, feedback, dashboard)
│   ├── chunking/                  # recursive character chunker
│   ├── embeddings/                # OpenAI embedding wrapper
│   ├── generation/                # context builder + answer generator
│   ├── ingestions/                # CSV / PDF / Markdown loaders + ingestion pipeline
│   ├── retrieval/                 # hybrid retriever (dense + BM25 + RRF + cross-encoder)
│   ├── dbops/                     # pgvector store
│   ├── services/                  # cache, fallback, web search, stats
│   └── utils/                     # tech detector, system stats
├── components/                    # sidebar, analytics bar, dashboard, feedback
├── benchmark/                     # RAGAS benchmark + results
└── styles/                        # CSS
```

---

## 🚀 Installation

```bash
git clone <repository-url>
cd dev-support

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file (see `.env.example` for the full list):

```env
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=your_base_url
OPENAI_MODEL=gpt-4o-mini
SERPER_API_KEY=your_serper_key   # optional, for web fallback
```

---

## 🐳 Database Setup

```bash
docker compose up -d
```

This starts a `pgvector/pgvector:pg17` container on port `5432`.

---

## ▶️ Running the Application

**Backend:**

```bash
uvicorn backend.api.main:app --reload
```

API docs: `http://localhost:8000/docs`

**Frontend:**

```bash
streamlit run app.py
```

App: `http://localhost:8501`

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask` | POST | Ask a technical question |
| `/upload` | POST | Upload and index a document |
| `/stats` | GET | Knowledge base statistics |
| `/dashboard` | GET | Full dashboard data |
| `/feedback` | POST | Submit answer feedback |

---

## 🧪 Running the Benchmark

With the backend running:

```bash
python benchmark/benchmark.py
```

Results are written to `benchmark/ragas_results.csv`.

---

## 🔮 Future Enhancements

- Trim agent prompt templates to raise Answer Relevancy toward 0.80+
- Expand the evaluation set beyond 18 questions
- Authentication & authorization
- Observability dashboard
- Multi-modal document support
