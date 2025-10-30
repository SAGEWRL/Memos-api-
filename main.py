from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid
import json
import os

app = FastAPI()

# ✅ Static & templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ Data file for storing API keys
DATA_FILE = "api_keys.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# ✅ Load keys from file
def load_keys():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# ✅ Save keys to file
def save_keys(keys):
    with open(DATA_FILE, "w") as f:
        json.dump(keys, f, indent=4)

# ✅ Homepage route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Generate new API key
@app.post("/generate-key")
async def generate_key(email: str = Form(...)):
    keys = load_keys()
    new_key = {
        "email": email,
        "key": str(uuid.uuid4())
    }
    keys.append(new_key)
    save_keys(keys)
    return {"message": "Key generated successfully", "key": new_key["key"]}

# ✅ Fetch all keys (for admin dashboard)
@app.get("/get-keys")
async def get_keys():
    return load_keys()

# ✅ Delete a key by value
@app.post("/delete-key")
async def delete_key(key: str = Form(...)):
    keys = load_keys()
    new_keys = [k for k in keys if k["key"] != key]
    save_keys(new_keys)
    return {"message": "Key deleted successfully"}

# ✅ Admin dashboard route
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})