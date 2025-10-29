from fastapi import FastAPI, HTTPException, Request, Securitypwfd
p[], Depends
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI(title="MemOS Memory API", version="4.0")

# 🔐 API Key setup
API_KEY = "12345SECRET"
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=401, detail="Missing or invalid API key")

# 🧩 Models
class SentimentRequest(BaseModel):
    text: str

# 🧠 Memory store
memory = []

# 💬 Analyze & store sentiment
@app.post("/sentiment/")
async def analyze_sentiment(data: SentimentRequest, api_key: APIKey = Depends(get_api_key)):
    sentiment_score = TextBlob(data.text).sentiment.polarity
    if sentiment_score > 0:
        sentiment = "positive"
    elif sentiment_score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Save to memory
    memory.append({"text": data.text, "sentiment": sentiment})

    return {"sentiment": sentiment, "memory_size": len(memory)}

# 🧠 Recall memory
@app.get("/memory/")
async def get_memory(api_key: APIKey = Depends(get_api_key)):
    return {"memory": memory, "total": len(memory)}
