from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import logging
from config.settings import (
    DATA_DIR, VECTOR_DB_DIR, PDF_FILES, EMBEDDING_MODEL,
    LLM_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, SIMILARITY_SEARCH_K,
    API_HOST, API_PORT
)
from src.rag.rag_system import RAGSystem

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG System API",
    description="Retrieval Augmented Generation API for document Q&A",
    version="1.0.0"
)

rag_system: Optional[RAGSystem] = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    answer: str
    status: str
    relevance_score: Optional[float] = None

@app.on_event("startup")
async def startup_event():
    global rag_system
    logger.info("Starting RAG System...")
    rag_system = RAGSystem(
        data_dir=DATA_DIR,
        vector_db_dir=VECTOR_DB_DIR,
        pdf_files=PDF_FILES,
        embedding_model=EMBEDDING_MODEL,
        llm_model=LLM_MODEL,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        similarity_k=SIMILARITY_SEARCH_K
    )
    if not rag_system.initialize():
        raise RuntimeError("Failed to initialize RAG system")
    logger.info("RAG System started successfully")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RAG API"}

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG System not initialized")
    
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        result = rag_system.query(request.query)
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("error"))
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "RAG System API",
        "docs": "/docs",
        "health": "/health",
        "query_endpoint": "/query"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=int(API_PORT))
