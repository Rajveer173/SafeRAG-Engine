from typing import Optional, List, Any
from pathlib import Path
import logging
from src.rag.core.loader import DocumentLoader
from src.rag.core.embeddings import EmbeddingManager
from src.rag.core.vector_store import VectorStoreManager
from src.rag.core.llm import LLMManager
from src.rag.core.utils import InputValidator, ResponseFormatter

logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(
        self,
        data_dir: Path,
        vector_db_dir: Path,
        pdf_files: List[str],
        embedding_model: str,
        llm_model: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        similarity_k: int = 3
    ) -> None:
        self.data_dir: Path = data_dir
        self.vector_db_dir: Path = vector_db_dir
        self.pdf_files: List[str] = pdf_files
        self.embedding_model: str = embedding_model
        self.llm_model: str = llm_model
        self.chunk_size: int = chunk_size
        self.chunk_overlap: int = chunk_overlap
        self.similarity_k: int = similarity_k
        
        self.document_loader: Optional[DocumentLoader] = None
        self.embedding_manager: Optional[EmbeddingManager] = None
        self.vector_store: Optional[VectorStoreManager] = None
        self.llm_manager: Optional[LLMManager] = None
        self.initialized: bool = False
    
    def initialize(self) -> bool:
        try:
            logger.info("=" * 50)
            logger.info("Initializing RAG System")
            logger.info("=" * 50)
            
            self.document_loader = DocumentLoader(self.data_dir)
            self.embedding_manager = EmbeddingManager(self.embedding_model)
            embeddings = self.embedding_manager.initialize()
            
            self.vector_store = VectorStoreManager(self.vector_db_dir, "resume_db")
            db = self.vector_store.load(embeddings)
            
            if db is None:
                logger.info("Building new vector store...")
                docs = self.document_loader.load_pdfs(self.pdf_files)
                chunks = self.document_loader.split_documents(
                    docs,
                    chunk_size=self.chunk_size,
                    chunk_overlap=self.chunk_overlap
                )
                self.vector_store.create(chunks, embeddings)
            
            self.llm_manager = LLMManager(self.llm_model)
            self.llm_manager.initialize()
            
            logger.info("RAG System initialized successfully")
            logger.info("=" * 50)
            self.initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG System: {str(e)}")
            return False
    
    def query(self, question: str) -> dict:
        if not self.initialized:
            logger.error("RAG System not initialized")
            return ResponseFormatter.format_error("System not initialized. Please restart.")
        
        if not InputValidator.validate_query(question):
            logger.warning(f"Invalid query: {question}")
            return ResponseFormatter.format_error("Invalid query. Please provide a valid question.")
        
        try:
            question = InputValidator.sanitize_query(question)
            results = self.vector_store.search(question, k=self.similarity_k)
            
            if len(results) == 0:
                logger.warning(f"No relevant content found for: {question}")
                context = "No relevant information found in documents."
            else:
                context = "\n---\n".join([doc.page_content for doc in results])
            
            prompt = f"""Based ONLY on the following context, answer the question accurately. If the answer is not in the context, say "Not in document".

Context:
{context}

Question: {question}

Answer:"""
            
            response = self.llm_manager.generate(prompt)
            
            return ResponseFormatter.format_answer(
                query=question,
                answer=response,
                relevance_score=None
            )
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return ResponseFormatter.format_error(f"Error: {str(e)}")
