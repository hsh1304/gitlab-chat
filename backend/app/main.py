import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retrieval import Retriever
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import requests
import openai

load_dotenv()

app = FastAPI(title="GenAI Chatbot - Local")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PDF_PATH = os.getenv("PDF_PATH", "/mnt/data/Project Brief_ GenAI Chatbot (1).pdf")
retriever = Retriever(pdf_path=PDF_PATH, chunk_size=200, overlap=50, top_k=3)

class ChatRequest(BaseModel):
    message: str
    use_llm: Optional[bool] = False
    llm_provider: Optional[str] = "openai"

class ChatResponse(BaseModel):
    answer: str
    source_texts: list

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message:
        raise HTTPException(status_code=400, detail="message required")

    hits = retriever.retrieve(req.message, top_k=3)

    context = "\n\n---\n\n".join([h["text"] for h in hits])

    if req.use_llm and req.llm_provider == "openai":
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise HTTPException(status_code=400, detail="OPENAI_API_KEY not set in env")
        openai.api_key = openai_api_key

        prompt = f"You are a helpful assistant. Use the context below to answer the question concisely.\n\nContext:\n{context}\n\nQuestion: {req.message}\n\nAnswer:"
        try:
            completion = openai.ChatCompletion.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.2,
            )
            answer = completion.choices[0].message.content.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")
    elif req.use_llm and req.llm_provider == "huggingface":
        hf_token = os.getenv("HF_TOKEN")
        hf_model = os.getenv("HF_MODEL", "gpt2")
        if not hf_token:
            raise HTTPException(status_code=400, detail="HF_TOKEN not set in env")
        prompt = f"Context:\n{context}\n\nQuestion: {req.message}\n\nAnswer:"
        headers = {"Authorization": f"Bearer {hf_token}"}
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}
        resp = requests.post(f"https://api-inference.huggingface.co/models/{hf_model}", headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Hugging Face error: {resp.text}")
        hf_out = resp.json()
        if isinstance(hf_out, dict) and "error" in hf_out:
            raise HTTPException(status_code=500, detail=hf_out["error"])
        answer = hf_out[0].get("generated_text", str(hf_out[0]))
    else:
        if not hits:
            answer = "I couldn't find any relevant information in the knowledge base for your question. Please try rephrasing your question or ask about GitLab features, CI/CD, project management, or security."
        else:
            answer = "Based on the GitLab Handbook, here's what I found:\n\n"
            for i, h in enumerate(hits, 1):
                # Only show the most relevant chunks
                if h.get('score', 0) > 0.1:  # Lowered threshold for better results
                    answer += f"**{i}.** {h['text']}\n\n"
            
            if not any(h.get('score', 0) > 0.1 for h in hits):
                answer = "I found some related information, but it may not be directly relevant to your question. Please try asking about specific GitLab features like CI/CD, project management, or security."

    return ChatResponse(answer=answer, source_texts=[h["text"] for h in hits])
