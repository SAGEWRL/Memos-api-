# main.py
from fastapi import FastAPI, HTTPException, Request, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from textblob import TextBlob
import os

# import key helper
from keys import init_db, generate_key_for, verify_key, increment_usage, list_keys, deactivate_key

# initialize DB on startup
init_db()

app = FastAPI(title="MemOS Memory API", version="5.0")

# ADMIN key from env (keep it secret). Set this on Render environment variables.
ADMIN_KEY = os.getenv("ADMIN_KEY", "12345SECRET")
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    # must provide header
    if not api_key_header:
        raise HTTPException(status_code=401, detail="Missing API key")

    # admin bypass
    if api_key_header == ADMIN_KEY:
        return api_key_header

    # verify user key from DB
    if verify_key(api_key_header):
        # increment usage for analytics/limits
        increment_usage(api_key_header)
        return api_key_header

    raise HTTPException(status_code=401, detail="Invalid or inactive API key")

# model for sentiment requests
class SentimentRequest(BaseModel):
    text: str

# in-memory memory for now (you can persist later)
memory = []

@app.post("/sentiment/")
async def analyze_sentiment(data: SentimentRequest, api_key: APIKey = Depends(get_api_key)):
    sentiment_score = TextBlob(data.text).sentiment.polarity
    if sentiment_score > 0:
        sentiment = "positive"
    elif sentiment_score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    memory.append({"text": data.text, "sentiment": sentiment})
    return {"sentiment": sentiment, "memory_size": len(memory)}

@app.get("/memory/")
async def get_memory(api_key: APIKey = Depends(get_api_key)):
    return {"memory": memory, "total": len(memory)}

# ======= Key management endpoints =======

# public signup: user supplies a desired username and receives an api_key
@app.post("/signup/")
async def signup(payload: dict):
    username = payload.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="username required")
    new_key = generate_key_for(username)
    return {"username": username, "api_key": new_key}

# admin route: generate a key for a username
@app.post("/generate-key/")
async def admin_generate_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Admin key required")
    body = await request.json()
    username = body.get("username") or "user"
    new_key = generate_key_for(username)
    return {"username": username, "api_key": new_key}

# admin route: list keys
@app.get("/keys/")
async def admin_list_keys(request: Request):
    key = request.headers.get("x-api-key")
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Admin key required")
    return {"keys": list_keys()}

# admin: deactivate a key
@app.post("/deactivate-key/")
async def admin_deactivate_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Admin key required")
    body = await request.json()
    target = body.get("target_key")
    if not target:
        raise HTTPException(status_code=400, detail="target_key required")
    ok = deactivate_key(target)
    return {"deactivated": ok, "target_key": target}