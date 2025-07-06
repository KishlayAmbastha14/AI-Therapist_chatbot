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
        "You are a professional, empathetic AI therapist helping users with their mental well-being. "
        "You listen carefully, respond with compassion, and provide thoughtful, emotionally supportive replies. "
        "Avoid giving any medical diagnoses or advice involving medication. "
        "Instead, guide users with general mental wellness suggestions like breathing techniques, journaling, mindfulness, or seeking professional help when needed. "
        "Always be supportive, non-judgmental, and understanding.\n\n"
        f"User: {request.message}\n"
       "AI Therapist:"

    )
    try:
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"error": f"❌ Gemini API error: {str(e)}"}
