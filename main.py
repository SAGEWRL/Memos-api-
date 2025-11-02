from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template setup
templates = Jinja2Templates(directory="templates")

# In-memory storage for generated keys (for demo)
generated_keys = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.post("/api/generate_key")
async def generate_key():
    key = uuid.uuid4().hex
    generated_keys[key] = {"active": True}
    return JSONResponse({"key": key})

@app.get("/api/verify_key/{key}")
async def verify_key(key: str):
    if key in generated_keys:
        return {"valid": True, "message": "Key is valid."}
    return {"valid": False, "message": "Invalid key."}