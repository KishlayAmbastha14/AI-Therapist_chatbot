from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (for frontend JS fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Serve the HTML page when visiting "/"
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse("index.html")

# ✅ ChatRequest model
class ChatRequest(BaseModel):
    message: str

# ✅ Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    prompt = (
      "You are a highly empathetic and professional AI therapist. Your role is to deeply understand the user's feelings and mental well-being concerns, respond with compassion, and provide long, reflective, emotionally supportive replies. "
      "Avoid giving any medical or diagnostic advice. "
      "Instead, offer general wellness suggestions like breathing exercises, journaling prompts, mindfulness techniques, and guidance to seek professional help when appropriate. "
      "Your responses should feel like a conversation with a warm, wise friend who truly listens and understands. "
      "Always be patient, non-judgmental, and aim to bring comfort and clarity. Respond in detail, elaborating on each point with care and kindness.\n\n"
      f"User: {request.message}\n"
      "AI Therapist:"
    )
    try:
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"error": f"❌ Gemini API error: {str(e)}"}
