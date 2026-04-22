import logging
import sys
from pathlib import Path
from config.settings import (
    DATA_DIR, VECTOR_DB_DIR, PDF_FILES, EMBEDDING_MODEL,
    LLM_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, SIMILARITY_SEARCH_K,
    LOG_LEVEL, LOG_FILE, LOG_FORMAT
)
from src.rag.rag_system import RAGSystem

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main() -> None:
    rag = RAGSystem(
        data_dir=DATA_DIR,
        vector_db_dir=VECTOR_DB_DIR,
        pdf_files=PDF_FILES,
        embedding_model=EMBEDDING_MODEL,
        llm_model=LLM_MODEL,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        similarity_k=SIMILARITY_SEARCH_K
    )
    
    if not rag.initialize():
        logger.error("Could not initialize RAG System. Exiting.")
        sys.exit(1)
    
    logger.info("Starting interactive Q&A session")
    print("\n" + "=" * 50)
    print("RAG Resume Query System")
    print("=" * 50)
    print("Type 'exit' to quit\n")
    
    while True:
        try:
            query = input("Ask something: ").strip()
            
            if query.lower() == 'exit':
                logger.info("User exited the session")
                print("\nGoodbye!")
                break
            
            if not query:
                print("Please enter a valid question.\n")
                continue
            
            print("\n" + "-" * 50)
            result = rag.query(query)
            
            if result.get("status") == "success":
                print(f"Answer:\n{result.get('answer')}")
            else:
                print(f"Error:\n{result.get('error')}")
            
            print("-" * 50 + "\n")
            
        except KeyboardInterrupt:
            logger.info("Session interrupted by user")
            print("\n\nSession ended.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {str(e)}")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
