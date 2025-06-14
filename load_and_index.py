# load_and_index.py
import json
from embed.vector_store import VectorIndex

def load_all_chunks():
    chunks = []

    with open("data/course_data.json", encoding="utf-8") as f:
        course_data = json.load(f)
        for slide in course_data:
            chunks.append({
                "source": "course",
                "text": slide["content_md"][:1000]  # truncate to 1k chars
            })

    with open("data/discourse_data.json", encoding="utf-8") as f:
        discourse_data = json.load(f)
        for post in discourse_data:
            chunks.append({
                "source": post["url"],
                "text": post["content"][:1000]
            })

    return chunks

if __name__ == "__main__":
    index = VectorIndex(dim=1536)
    all_chunks = load_all_chunks()
    index.add_documents(all_chunks)
    print(f"✅ Indexed {len(all_chunks)} documents")
