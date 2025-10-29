import sqlite3
import uuid

# Initialize or connect to database
conn = sqlite3.connect("keys.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE,
    active INTEGER DEFAULT 1
)
""")
conn.commit()

def generate_key():
    new_key = str(uuid.uuid4())
    cursor.execute("INSERT INTO api_keys (key) VALUES (?)", (new_key,))
    conn.commit()
    return new_key

def verify_key(user_key):
    cursor.execute("SELECT * FROM api_keys WHERE key=? AND active=1", (user_key,))
    return cursor.fetchone() is not None

def deactivate_key(user_key):
    cursor.execute("UPDATE api_keys SET active=0 WHERE key=?", (user_key,))
    conn.commit()

# Example usage
if __name__ == "__main__":
    print("Generated key:", generate_key())
