import re

def chunk_all_texts(texts, chunk_size=300, overlap=50):
    """
    Splits a list of strings into overlapping chunks.
    
    Args:
        texts (List[str]): List of documents.
        chunk_size (int): Number of words per chunk.
        overlap (int): Number of overlapping words between chunks.
    
    Returns:
        List[str]: List of chunked text.
    """
    chunks = []
    for text in texts:
        words = re.findall(r'\S+', text)
        i = 0
        while i < len(words):
            chunk = words[i:i+chunk_size]
            chunks.append(' '.join(chunk))
            i += chunk_size - overlap
    return chunks
