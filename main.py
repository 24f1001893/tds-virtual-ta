from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json

from embed import vector_store
from embed.embedder import get_embedding
from embed.utils import chunk_all_texts  # optional

load_dotenv()

app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    image: str = None

@app.on_event("startup")
async def load_documents():
    with open("data/course_data.json") as f:
        course_data = json.load(f)
    with open("data/discourse_data.json") as f:
        discourse_data = json.load(f)

    all_chunks = []
    for slide in course_data:
        all_chunks.append({"source": "course", "text": slide["content_md"][:1000]})
    for post in discourse_data:
        all_chunks.append({"source": post["url"], "text": post["content"][:1000]})

    vector_store.add_documents(all_chunks)

@app.post("/api/")
async def ask_virtual_ta(q: QuestionRequest):
    top_chunks = vector_store.search(q.question, k=3)
    context = "\n\n---\n\n".join([c["text"] for c in top_chunks])

    # ✅ Dummy but context-based answer
    dummy_answer = f"""
I'm a virtual TA. Here's an answer based on your question and the most relevant course content:

**Question:** {q.question}

**Answer:** Based on the materials, it appears that:
{context[:500]}...

(Answer generated from context above. For full details, please refer to the course materials or forum discussions.)
"""

    return {
        "answer": dummy_answer.strip(),
        "links": [
            {"url": c["source"], "text": c["source"]} for c in top_chunks if c["source"].startswith("http")
        ]
    }
