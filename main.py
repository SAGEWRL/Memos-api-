from fastapi import FastAPI, HTTPException, Depends, Security, Request
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from textblob import TextBlob
import secrets

app = FastAPI(title="MemOS Memory API", version="4.2")

# 🔐 API Keys
ADMIN_KEY = "ADMIN-12345SECRET"
USER_KEYS = ["USER-abc123", "USER-xyz456"]

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Serve static + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == ADMIN_KEY:
        return {"type": "admin", "key": api_key_header}
    elif api_key_header in USER_KEYS:
        return {"type": "user", "key": api_key_header}
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

# 🧩 Models
class SentimentRequest(BaseModel):
    text: str

memory = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/sentiment/")
async def analyze_sentiment(data: SentimentRequest, api_key: dict = Depends(get_api_key)):
    sentiment_score = TextBlob(data.text).sentiment.polarity
    sentiment = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
    memory.append({"text": data.text, "sentiment": sentiment})
    return {"sentiment": sentiment, "memory_size": len(memory)}

@app.get("/memory/")
async def get_memory(api_key: dict = Depends(get_api_key)):
    return {"memory": memory, "total": len(memory)}

@app.delete("/admin/clear/")
async def clear_memory(api_key: dict = Depends(get_api_key)):
    if api_key["type"] != "admin":
        raise HTTPException(status_code=403, detail="Admin key required")
    memory.clear()
    return {"message": "Memory cleared successfully", "total": len(memory)}

# 🧠 Generate new user API keys
@app.post("/api/generate_key")
async def generate_api_key():
    new_key = "USER-" + secrets.token_hex(4)
    USER_KEYS.append(new_key)
    return {"key": new_key}