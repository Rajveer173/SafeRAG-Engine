from typing import Any
import logging

logger = logging.getLogger(__name__)

class EmbeddingManager:
    def __init__(self, model_name: str) -> None:
        self.model_name: str = model_name
        self.embeddings: Any = None
    
    def initialize(self) -> Any:
        try:
            from langchain_ollama import OllamaEmbeddings
            logger.info(f"Initializing embeddings with model: {self.model_name}")
            self.embeddings = OllamaEmbeddings(model=self.model_name)
            logger.info("Embeddings initialized successfully")
            return self.embeddings
        except Exception as e:
            logger.error(f"Error initializing embeddings: {str(e)}")
            logger.error("Make sure Ollama is running with: ollama serve")
            raise
    
    def get_embeddings(self) -> Any:
        if self.embeddings is None:
            return self.initialize()
        return self.embeddings
