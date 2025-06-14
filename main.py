from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QuestionRequest(BaseModel):
    question: str
    image: str = None

@app.post("/api/")
async def ask_virtual_ta(request: QuestionRequest):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual TA for IIT Madras TDS course. Answer helpfully."},
                {"role": "user", "content": request.question}
            ]
        )

        answer = completion.choices[0].message.content.strip()

        return {
            "answer": answer,
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/t/example-post",
                    "text": "Example supporting link"
                }
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
