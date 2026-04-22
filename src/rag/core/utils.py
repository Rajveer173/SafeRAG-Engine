from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class InputValidator:
    @staticmethod
    def validate_query(query: str, min_length: int = 3) -> bool:
        if not query or not isinstance(query, str):
            logger.warning("Invalid query: empty or not a string")
            return False
        if len(query.strip()) < min_length:
            logger.warning(f"Query too short: {len(query.strip())} < {min_length}")
            return False
        return True
    
    @staticmethod
    def sanitize_query(query: str) -> str:
        return query.strip()

class ResponseFormatter:
    @staticmethod
    def format_answer(query: str, answer: str, relevance_score: Optional[float] = None) -> dict:
        return {
            "query": query,
            "answer": answer,
            "relevance_score": relevance_score,
            "status": "success"
        }
    
    @staticmethod
    def format_error(error_msg: str) -> dict:
        return {
            "error": error_msg,
            "status": "error"
        }
