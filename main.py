from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from textblob import TextBlob
import secrets
import json
import os

app = FastAPI()

# ✅ Mount static and templates folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ Path for saving API keys
DATA_FILE = "api_keys.json"


# 🏠 Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 🔑 Generate API Key
@app.post("/generate_key")
async def generate_key(email: str = Form(...)):
    key = secrets.token_hex(16)

    # Load old data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Save new key
    data[email] = {"key": key, "usage": 0}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {"success": True, "key": key}


# 🧠 Text Sentiment Analysis
@app.post("/analyze_text")
async def analyze_text(text: str = Form(...)):
    if not text.strip():
        return {"error": "No text provided"}

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        mood = "Positive 😄"
    elif polarity < 0:
        mood = "Negative 😞"
    else:
        mood = "Neutral 😐"

    return {"mood": mood, "score": polarity}


# 🧩 Admin Dashboard
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    if not os.path.exists(DATA_FILE):
        users = {}
    else:
        with open(DATA_FILE, "r") as f:
            users = json.load(f)

    return templates.TemplateResponse("admin.html", {"request": request, "users": users})


# 🚀 Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)