from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import secrets

# Initialize FastAPI app
app = FastAPI()

# Serve static and template files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 🏠 Home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 🔑 API route to generate random keys
@app.post("/api/generate_key")
async def generate_key():
    try:
        key = secrets.token_hex(16)  # Generate a 32-character key
        return JSONResponse(content={"success": True, "key": key})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)})

# 🧭 Admin route (optional for later)
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})