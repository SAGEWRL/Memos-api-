from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import firebase_admin
from firebase_admin import credentials, db
import secrets

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Initialize Firebase
# Make sure this file exists in your project root (same folder as main.py)
cred = credentials.Certificate("memos-service.json")  # ← Your service account file name
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://memos-api-default-rtdb.firebaseio.com/"  # ← Your Firebase DB URL
})

# ✅ Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ Home page (index.html)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Admin dashboard
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# ✅ API: Generate key and store it in Firebase
@app.post("/api/generate_key")
async def generate_key():
    new_key = secrets.token_hex(16)
    ref = db.reference("api_keys")
    ref.push({
        "key": new_key,
        "status": "active"
    })
    return JSONResponse({"success": True, "key": new_key})

# ✅ API: Validate key
@app.get("/api/validate/{key}")
async def validate_key(key: str):
    ref = db.reference("api_keys")
    keys = ref.get()

    if keys:
        for _, data in keys.items():
            if data.get("key") == key and data.get("status") == "active":
                return {"valid": True, "message": "✅ Key is valid and active"}
    return {"valid": False, "message": "❌ Invalid or inactive key"}

# ✅ Fallback route
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "MemOs API running perfectly"}

# ✅ Run (local only)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)