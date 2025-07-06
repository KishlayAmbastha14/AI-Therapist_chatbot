# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import google.generativeai as genai
# import os

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model = genai.GenerativeModel("gemini-2.5-pro")


# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class ChatRequest(BaseModel):
#     message: str

# # ✅ Root test route
# @app.get("/")
# def read_root():
#     return {"message": "✅ Gemini Health Assistant API is running."}

# # ✅ Chat endpoint
# @app.post("/chat")
# def chat(request: ChatRequest):
#     prompt = (
#       "You are a kind, empathetic AI therapist. Respond to the user's concern using short (2–3 sentence), emotionally supportive, clear language. "
#       "Avoid technical terms or medical advice. Focus on simple wellness suggestions like breathing, journaling, or mindfulness. "
#       "Keep responses short, warm, and easy to understand.\n\n"
#       f"User: {request.message}\n"
#       "AI Therapist:"
#     )
#     try:
#         response = model.generate_content(prompt)
#         return {"reply": response.text}
#     except Exception as e:
#         return {"error": f"❌ Gemini API error: {str(e)}"}





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
