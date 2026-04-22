from typing import Any
import logging

logger = logging.getLogger(__name__)

class LLMManager:
    def __init__(self, model_name: str, temperature: float = 0.7) -> None:
        self.model_name: str = model_name
        self.temperature: float = temperature
        self.llm: Any = None
    
    def initialize(self) -> Any:
        try:
            from langchain_ollama import OllamaLLM
            logger.info(f"Initializing LLM with model: {self.model_name}")
            self.llm = OllamaLLM(model=self.model_name, temperature=self.temperature)
            logger.info("LLM initialized successfully")
            return self.llm
        except Exception as e:
            logger.error(f"Error initializing LLM: {str(e)}")
            raise
    
    def get_llm(self) -> Any:
        if self.llm is None:
            return self.initialize()
        return self.llm
    
    def generate(self, prompt: str) -> str:
        try:
            llm = self.get_llm()
            logger.info("Generating response...")
            response = llm.invoke(prompt)
            logger.info("Response generated successfully")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
