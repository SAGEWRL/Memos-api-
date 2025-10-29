import sqlite3
from textblob import TextBlob
from datetime import datetime

def update_priorities():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("SELECT id, content FROM memories")
    rows = c.fetchall()

    for r in rows:
        text = r[1]
        score = len(text) * (TextBlob(text).sentiment.polarity + 1)
        c.execute("UPDATE memories SET tags = tags || ',priority:' || ? WHERE id=?", (round(score, 2), r[0]))
    
    conn.commit()
    conn.close()
    return "Priorities updated"

def reflect():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("SELECT content FROM memories")
    data = [r[0] for r in c.fetchall()]
    conn.close()
    if not data:
        return "No memories yet."
    blob = TextBlob(" ".join(data))
    summary = blob.noun_phrases[:5]
    return {"insight": f"Your current focus seems around: {', '.join(summary)}"}
