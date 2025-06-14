from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from embed import vector_store
from embed.embedder import get_embedding
from embed.utils import chunk_all_texts  # optional, if needed for chunking

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    #vector_store.add_documents(all_chunks)

@app.post("/api/")
async def ask_virtual_ta(q: QuestionRequest):
    top_chunks = vector_store.search(q.question, k=3)
    context = "\n---\n".join([c["text"] for c in top_chunks])

    messages = [
        {"role": "system", "content": "You are a helpful teaching assistant for the Tools in Data Science course."},
        {"role": "user", "content": f"Question: {q.question}\n\nRelevant material:\n{context}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3
    )

    return {
        "answer": response.choices[0].message.content.strip(),
        "links": [
            {"url": c["source"], "text": c["source"]} for c in top_chunks if c["source"].startswith("http")
        ]
    }
