# keys.py
import sqlite3
import secrets
from datetime import datetime

DB = "keys.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key TEXT UNIQUE,
        username TEXT,
        active INTEGER DEFAULT 1,
        usage_count INTEGER DEFAULT 0,
        created_at TEXT
    );
    """)
    conn.commit()
    conn.close()

def generate_key_for(username: str) -> str:
    init_db()
    new_key = secrets.token_hex(24)  # 48 hex chars
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO api_keys (api_key, username, created_at) VALUES (?, ?, ?)",
        (new_key, username, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return new_key

def verify_key(key: str) -> bool:
    init_db()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT active FROM api_keys WHERE api_key=? LIMIT 1", (key,))
    row = c.fetchone()
    conn.close()
    return bool(row and row[0] == 1)

def increment_usage(key: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE api_keys SET usage_count = usage_count + 1 WHERE api_key=?", (key,))
    conn.commit()
    conn.close()

def list_keys():
    init_db()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT api_key, username, active, usage_count, created_at FROM api_keys")
    rows = c.fetchall()
    conn.close()
    return [{"api_key": r[0], "username": r[1], "active": r[2], "usage": r[3], "created_at": r[4]} for r in rows]

def deactivate_key(key: str) -> bool:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE api_keys SET active=0 WHERE api_key=?", (key,))
    conn.commit()
    changed = c.rowcount
    conn.close()
    return changed > 0

# optional: quick test when run directly
if __name__ == "__main__":
    init_db()
    print("DB init done. Example key:", generate_key_for("test"))