import pytest
from pathlib import Path
from src.rag.core.utils import InputValidator, ResponseFormatter

class TestInputValidator:
    def test_valid_query(self):
        assert InputValidator.validate_query("What is your experience?") == True
    
    def test_empty_query(self):
        assert InputValidator.validate_query("") == False
    
    def test_short_query(self):
        assert InputValidator.validate_query("hi") == False
    
    def test_none_query(self):
        assert InputValidator.validate_query(None) == False
    
    def test_sanitize_query(self):
        assert InputValidator.sanitize_query("  hello world  ") == "hello world"

class TestResponseFormatter:
    def test_format_answer(self):
        result = ResponseFormatter.format_answer("What is this?", "This is an answer")
        assert result["status"] == "success"
        assert result["query"] == "What is this?"
        assert result["answer"] == "This is an answer"
    
    def test_format_error(self):
        result = ResponseFormatter.format_error("Test error")
        assert result["status"] == "error"
        assert result["error"] == "Test error"
