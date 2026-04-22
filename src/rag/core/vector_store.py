from typing import Optional, List, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self, db_dir: Path, db_name: str) -> None:
        self.db_dir: Path = db_dir
        self.db_name: str = db_name
        self.db: Optional[Any] = None
    
    def create(self, chunks: list, embeddings: Any) -> Any:
        try:
            from langchain_community.vectorstores import Chroma
            logger.info("Creating vector store from chunks...")
            self.db = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=str(self.db_dir / self.db_name)
            )
            self.db.persist()
            logger.info(f"Vector store created and persisted at {self.db_dir / self.db_name}")
            return self.db
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def load(self, embeddings: Any) -> Optional[Any]:
        db_path = self.db_dir / self.db_name
        
        if not db_path.exists():
            logger.warning(f"Vector store not found at {db_path}")
            return None
        
        try:
            from langchain_community.vectorstores import Chroma
            logger.info(f"Loading vector store from {db_path}")
            self.db = Chroma(
                persist_directory=str(db_path),
                embedding_function=embeddings
            )
            logger.info("Vector store loaded successfully")
            return self.db
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return None
    
    def search(self, query: str, k: int = 3) -> List[Any]:
        if self.db is None:
            raise RuntimeError("Vector store not initialized")
        
        try:
            logger.info(f"Searching vector store with query: {query}")
            results = self.db.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} relevant chunks")
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            raise
    
    def get_db(self) -> Optional[Any]:
        return self.db
