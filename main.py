from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

# Allow your website to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your actual website domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client (make sure your API key is set in your server environment variables)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    user_msg = request.message
    
    # System prompt giving the AI context about Monet Online School
    system_instruction = (
        "You are Monet Online School's friendly AI academic advisor. "
        "You help parents find the right teacher for their child. "
        "Our teachers include: Abigail Temile (Mathematics and English Specialist, 3 years experience), "
        "Caroline Adeniji (Mathematics Specialist, 10 years experience, focuses on preschool to Grade 3), "
        "and Onyinyechi Bibian (English Specialist in Reading, Phonics, Grammar, Vocabulary, and Verbal Reasoning, 5 years experience). "
        "Keep your answers concise, helpful, and friendly."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_msg}
            ]
        )
        ai_reply = response.choices[0].message.content
        return {"reply": ai_reply}
        
    except Exception as e:
        return {"reply": "I'm having a little trouble connecting right now. Please try again later!"}