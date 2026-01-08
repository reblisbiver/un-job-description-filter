import os
import sys
import shutil
import tempfile
import json
import logging
from datetime import datetime
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .parser import JDParser

# Setup local debug logging
if getattr(sys, 'frozen', False):
    LOG_PATH = os.path.join(os.path.dirname(sys.executable), "server_debug.log")
else:
    LOG_PATH = "server_debug.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="UN JD Parser")

# Add CORS middleware to help with "Failed to fetch"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determine the base path for storage (persistent next to .exe)
if getattr(sys, 'frozen', False):
    # If running as a bundled exe, use the directory of the exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # If running in development, use the project root
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STORAGE_DIR = os.path.join(BASE_DIR, "storage")
STORAGE_FILE = os.path.join(STORAGE_DIR, "data.json")
FILES_DIR = os.path.join(STORAGE_DIR, "files")

try:
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR, exist_ok=True)
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR, exist_ok=True)
    logging.info(f"Storage directories check/create at: {STORAGE_DIR}")
except Exception as e:
    logging.error(f"FATAL: Could not create storage directory: {e}")

def load_data():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error reading JSON: {e}")
    return []

def save_data(data):
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error saving JSON: {e}")

# Determine the path for static files (internal to bundle)
if getattr(sys, 'frozen', False):
    INNER_BASE = sys._MEIPASS
    static_dir = os.path.join(INNER_BASE, "app", "static")
else:
    INNER_BASE = os.path.dirname(__file__)
    static_dir = os.path.join(INNER_BASE, "static")

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")
# Mount storage/files to allow browser access to saved PDFs/Docs
app.mount("/files", StaticFiles(directory=FILES_DIR), name="files")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/history")
async def get_history():
    return load_data()

@app.post("/toggle-finished/{uid}")
async def toggle_finished(uid: str):
    """Toggle the 'finished' status for a JD entry using its unique safe filename."""
    data = load_data()
    for item in data:
        if item.get("saved_filename") == uid:
            item["finished"] = not item.get("finished", False)
            save_data(data)
            return {"status": "success", "finished": item["finished"]}
    return {"status": "error", "message": "not found"}

@app.post("/delete/{uid}")
async def delete_job(uid: str):
    """Delete a JD entry and its physical file using its unique safe filename."""
    data = load_data()
    new_data = []
    found = False
    
    for item in data:
        if item.get("saved_filename") == uid:
            found = True
            # Delete physical file
            file_path = os.path.join(FILES_DIR, uid)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logging.info(f"Deleted physical file: {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete physical file {file_path}: {e}")
            continue # Skip adding this item to new_data
        new_data.append(item)
    
    if found:
        save_data(new_data)
        return {"status": "success"}
    return {"status": "error", "message": "JD not found"}

@app.post("/parse")
async def parse_jds(files: List[UploadFile] = File(...)):
    """
    Parse multiple uploaded JD files, save files locally, and save info to storage.
    """
    logging.info(f"Request: Parse {len(files)} files")
    try:
        new_results = []
        existing_data = load_data()
        
        for file in files:
            logging.info(f"Processing file: {file.filename}")
            if not file.filename.lower().endswith(('.pdf', '.docx')):
                continue
            
            # Save file to STORAGE/FILES_DIR
            file_ext = os.path.splitext(file.filename)[1]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_filename = f"{timestamp}{file_ext}"
            save_path = os.path.join(FILES_DIR, safe_filename)
            
            try:
                with open(save_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                info = JDParser.parse_file(save_path)
                info["filename"] = file.filename
                info["saved_filename"] = safe_filename
                info["upload_time"] = datetime.now().isoformat()
                info["finished"] = False
                if info.get("id") == "N/A":
                    info["id"] = safe_filename
                new_results.append(info)
                logging.info(f"Successfully parsed: {file.filename}")
            except Exception as parse_err:
                logging.error(f"Parsing error for {file.filename}: {parse_err}")
                new_results.append({
                    "filename": file.filename,
                    "saved_filename": safe_filename,
                    "job_title": f"Parsing Error: {str(parse_err)}",
                    "upload_time": datetime.now().isoformat(),
                    "finished": False,
                    "id": safe_filename
                })
        
        updated_data = new_results + existing_data
        save_data(updated_data)
        return updated_data
    except Exception as e:
        logging.error(f"Global /parse exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
