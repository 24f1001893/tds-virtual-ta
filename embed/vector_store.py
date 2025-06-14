# embed/vector_store.py
import chromadb
from embed.embedder import get_embedding

chroma_client = chromadb.Client()
collection = chromadb.Client().create_collection(name="tds_chunks")

def add_documents(chunks):
    for i, chunk in enumerate(chunks):
        text = chunk["text"]
        source = chunk["source"]
        embedding = get_embedding(text)

        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[str(i)],
            metadatas=[{"source": source}]
        )

def search(query, k=3):
    query_embedding = get_embedding(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=k)

    matches = []
    for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
        matches.append({
            "text": doc,
            "source": metadata["source"]
        })
    return matches
