from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text: str, size: int = 300, overlap: int = 50) -> List[str]:
    """
    Splits the text into chunks of specified size with overlap.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,  # ≈ 250–300 tokens
        chunk_overlap=overlap,  # keeps context
        separators=["\n\n", "\n", ".", " ", ""],
    )
    
    return text_splitter.split_text(text)
