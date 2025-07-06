from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyBueTIb5BkI7gzONFbzbkVb20YTjBJ39r8")

# ✅ Load the model
model = genai.GenerativeModel("gemini-2.5-pro")

# ✅ FastAPI app setup
app = FastAPI()

# ✅ Enable CORS (for frontend testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request schema
class ChatRequest(BaseModel):
    message: str

# ✅ Root test route
@app.get("/")
def read_root():
    return {"message": "✅ Gemini Health Assistant API is running."}

# ✅ Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    prompt = (
      "You are a kind, empathetic AI therapist. Respond to the user's concern using short (2–3 sentence), emotionally supportive, clear language. "
      "Avoid technical terms or medical advice. Focus on simple wellness suggestions like breathing, journaling, or mindfulness. "
      "Keep responses short, warm, and easy to understand.\n\n"
      f"User: {request.message}\n"
      "AI Therapist:"
    )
    try:
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"error": f"❌ Gemini API error: {str(e)}"}