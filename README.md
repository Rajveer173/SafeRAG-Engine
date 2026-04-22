# RAG System - Retrieval-Augmented Generation

A production-grade Retrieval-Augmented Generation (RAG) system that combines document retrieval with large language models to answer questions based on your data.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-green)
![LangChain](https://img.shields.io/badge/LangChain-1.2+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Real-time Document Processing** - Load and process PDF documents on-the-fly
- **Vector Embeddings** - Convert text to semantic vectors using Ollama
- **Similarity Search** - Find relevant document chunks using ChromaDB
- **AI-Powered Responses** - Generate contextual answers using llama3
- **REST API** - FastAPI endpoint for programmatic access
- **CLI Interface** - Interactive command-line for testing
- **Type Safety** - Full type hints throughout codebase
- **Comprehensive Logging** - Debug and monitor system behavior
- **Docker Support** - Containerized deployment ready
- **CI/CD Pipelines** - Automated testing and quality checks


## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai) installed and running
- Docker & Docker Compose (optional)

### Ollama Models Required
```bash
ollama pull nomic-embed-text    # For embeddings
ollama pull llama3              # For generation
```

##  Start application

### 1. Clone Repository
```bash
git clone https://github.com/Rajveer173/SafeRAG-Engine.git
cd rag
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your PDF
Place your PDF file in the `data/` directory:
```
data/
└── data.pdf
```

### 5. Run CLI
```bash
python cli.py
```

Ask your questions:
```
Ask something: What features does the system have?
Answer: ...
```

## 📡 REST API

### Start Server
```bash
python -m uvicorn src.rag.api.server:app --reload
```

Server runs at: `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Query Document
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic?"}'
```

**Response:**
```json
{
  "query": "What is the main topic?",
  "answer": "The main topic is...",
  "status": "success",
  "retrieval_context": "..."
}
```

### Interactive API Docs
Visit: `http://localhost:8000/docs`

## Docker Deployment

### Option 1: Docker Compose
```bash
docker-compose up --build
```

Starts:
- RAG API on port 8000
- Ollama service
- Auto-initializes models

### Option 2: Docker Image
```bash
docker build -f docker/Dockerfile -t rag-system:latest .
docker run -p 8000:8000 rag-system:latest
```

## Performance

- **Document Processing**: ~2 seconds for 2-page PDF
- **Query Response Time**: 10-15 seconds (includes LLM generation)
- **Vector Search**: <500ms
- **Throughput**: Handle 100+ concurrent queries



## License

This project is licensed under the MIT License - see LICENSE file for details.



**Built with ❤️ by Rajveer**


