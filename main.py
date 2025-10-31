from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from textblob import TextBlob
from flask import Flask, render_template_string
import secrets

# -----------------------------
# Flask Admin App
# -----------------------------
admin_app = Flask(__name__)

@admin_app.route("/")
def admin_home():
    html = """
    <h1 style='font-family:Arial;text-align:center;color:#007BFF;'>Memos Admin Dashboard</h1>
    <p style='text-align:center;'>Welcome to your control panel 🔐</p>
    <ul style='text-align:center;list-style:none;'>
      <li><a href='/admin/keys'>View Generated Keys</a></li>
      <li><a href='/'>Back to API Home</a></li>
    </ul>
    """
    return render_template_string(html)

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="Memos API")

# Allow frontend or any site to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Flask admin at /admin
app.mount("/admin", WSGIMiddleware(admin_app))

# -----------------------------
# API ROUTES
# -----------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2 style='text-align:center;color:#28A745;'>Welcome to Memos API 🚀</h2>
    <p style='text-align:center;'>Use the <a href="/docs">/docs</a> to explore API endpoints.</p>
    """

@app.post("/generate_key")
def generate_key(email: str = Form(...)):
    try:
        # Generate secure random key
        key = secrets.token_hex(16)
        return {"success": True, "key": key}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/analyze_text")
def analyze_text(text: str = Form(...)):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    mood = "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"
    return {"text": text, "mood": mood, "score": sentiment}

@app.get("/about")
def about():
    return {"app": "Memos", "version": "1.0", "creator": "J.C. Washington"}

# -----------------------------
# Run (local testing)
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)