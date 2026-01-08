import os
import sys
import threading
import uvicorn
import webview
import requests
from time import sleep

# Fix for PyInstaller windowed mode where stdout/stderr are None
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

# Import the FastAPI app
from app.main import app

def run_server():
    """Function to run the FastAPI server."""
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "%(levelprefix)s %(message)s"
    log_config["formatters"]["access"]["fmt"] = '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8542, 
        log_level="error",
        log_config=log_config
    )

if __name__ == "__main__":
    # Start FastAPI in a separate thread (more stable than multiprocessing for PyInstaller)
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for server to start up by polling the health endpoint or just sleeping
    # Polling is safer
    retries = 10
    while retries > 0:
        try:
            response = requests.get("http://127.0.0.1:8542/history", timeout=1)
            if response.status_code == 200:
                break
        except:
            pass
        sleep(0.5)
        retries -= 1

    # Create a native window pointing to the local FastAPI server
    try:
        webview.create_window(
            'UN JD Filter & Parser', 
            'http://127.0.0.1:8542',
            width=1200,
            height=800,
            min_size=(800, 600)
        )
        webview.start()
    except Exception as e:
        # Fallback to console error if webview fails
        with open("error_log.txt", "a") as f:
            f.write(f"GUI Error: {str(e)}\n")
