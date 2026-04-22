from typing import List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DocumentLoader:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir: Path = data_dir
    
    def load_pdfs(self, file_names: List[str]) -> list:
        from langchain_community.document_loaders import PyPDFLoader
        
        all_docs = []
        for pdf_file in file_names:
            pdf_path = self.data_dir / pdf_file
            
            if not pdf_path.exists():
                logger.warning(f"PDF file not found: {pdf_path}")
                continue
            
            try:
                logger.info(f"Loading PDF: {pdf_file}")
                loader = PyPDFLoader(str(pdf_path))
                docs = loader.load()
                logger.info(f"Loaded {len(docs)} pages from {pdf_file}")
                all_docs.extend(docs)
            except Exception as e:
                logger.error(f"Error loading PDF {pdf_file}: {str(e)}")
                continue
        
        if not all_docs:
            raise ValueError("No documents loaded")
        
        return all_docs
    
    def split_documents(self, docs: list, chunk_size: int = 500, chunk_overlap: int = 50) -> list:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        try:
            logger.info(f"Splitting {len(docs)} documents into chunks...")
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            chunks = splitter.split_documents(docs)
            logger.info(f"Created {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            raise
