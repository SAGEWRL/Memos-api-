from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from textblob import TextBlob
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="MemOS Memory API", version="4.2")

# ------------------ DATABASE SETUP ------------------
DATABASE_URL = "sqlite:///./memory.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ SECURITY SETUP ------------------
ADMIN_KEY = "ADMIN-12345SECRET"
USER_KEYS = ["USER-abc123", "USER-xyz456"]
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == ADMIN_KEY:
        return {"type": "admin", "key": api_key_header}
    elif api_key_header in USER_KEYS:
        return {"type": "user", "key": api_key_header}
    else:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

# ------------------ MODELS ------------------
class SentimentRequest(BaseModel):
    text: str

# ------------------ ROUTES ------------------
@app.post("/sentiment/")
async def analyze_sentiment(data: SentimentRequest, api_key: dict = Depends(get_api_key), db=Depends(get_db)):
    sentiment_score = TextBlob(data.text).sentiment.polarity
    sentiment = (
        "positive" if sentiment_score > 0 else
        "negative" if sentiment_score < 0 else
        "neutral"
    )

    new_memory = Memory(text=data.text, sentiment=sentiment)
    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)

    return {"sentiment": sentiment, "id": new_memory.id}


@app.get("/memory/")
async def get_memory(api_key: dict = Depends(get_api_key), db=Depends(get_db)):
    memories = db.query(Memory).all()
    return {"memory": [{"text": m.text, "sentiment": m.sentiment} for m in memories], "total": len(memories)}


@app.delete("/admin/clear/")
async def clear_memory(api_key: dict = Depends(get_api_key), db=Depends(get_db)):
    if api_key["type"] != "admin":
        raise HTTPException(status_code=403, detail="Admin key required")

    db.query(Memory).delete()
    db.commit()
    return {"message": "Memory cleared successfully"}