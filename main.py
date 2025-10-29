from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from textblob import TextBlob
import secrets

app = FastAPI(title="MemOS Memory API", version="5.0")

# 🔐 In-memory key store
ADMIN_KEY = "ADMIN-12345SECRET"
user_keys = ["USER-abc123", "USER-xyz456"]  # Starts with a few default ones
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# 🧠 Memory store
memory = []

# 🔑 API key validation
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == ADMIN_KEY:
        return {"type": "admin", "key": api_key_header}
    elif api_key_header in user_keys:
        return {"type": "user", "key": api_key_header}
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

# 🧩 Models
class SentimentRequest(BaseModel):
    text: str

class NewKeyRequest(BaseModel):
    role: str  # "user" or "admin"

# 💬 Analyze sentiment
@app.post("/sentiment/")
async def analyze_sentiment(data: SentimentRequest, api_key: dict = Depends(get_api_key)):
    sentiment_score = TextBlob(data.text).sentiment.polarity
    sentiment = (
        "positive" if sentiment_score > 0 else
        "negative" if sentiment_score < 0 else
        "neutral"
    )
    memory.append({"text": data.text, "sentiment": sentiment})
    return {"sentiment": sentiment, "memory_size": len(memory)}

# 🧠 Get memory
@app.get("/memory/")
async def get_memory(api_key: dict = Depends(get_api_key)):
    return {"memory": memory, "total": len(memory)}

# 🔧 Admin: Clear memory
@app.delete("/admin/clear/")
async def clear_memory(api_key: dict = Depends(get_api_key)):
    if api_key["type"] != "admin":
        raise HTTPException(status_code=403, detail="Admin key required")
    memory.clear()
    return {"message": "Memory cleared successfully", "total": len(memory)}

# 🪪 Admin: Generate new API key
@app.post("/admin/generate-key/")
async def generate_key(req: NewKeyRequest, api_key: dict = Depends(get_api_key)):
    if api_key["type"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can generate keys")

    new_key = f"{req.role.upper()}-{secrets.token_hex(8)}"
    if req.role.lower() == "user":
        user_keys.append(new_key)
    elif req.role.lower() == "admin":
        global ADMIN_KEY
        ADMIN_KEY = new_key
    else:
        raise HTTPException(status_code=400, detail="Role must be 'user' or 'admin'")

    return {"new_key": new_key, "role": req.role}