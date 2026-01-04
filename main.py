from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import subprocess, os, uuid, urllib.parse

# Developer info
DEVELOPER = "SAIFUL ISLAM"
CONTACT = "Telegram: @saifulmn"

# Directories
BASE_DIR = "downloads"
VIDEO_DIR = f"{BASE_DIR}/video"
MP3_DIR = f"{BASE_DIR}/mp3"

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(MP3_DIR, exist_ok=True)

app = FastAPI(
    title="YouTube Downloader API",
    description=f"FastAPI + yt-dlp (Render ready)\nDeveloper: {DEVELOPER}\nContact: {CONTACT}",
    version="1.0"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "developer": DEVELOPER,
        "contact": CONTACT,
        "endpoints": {
            "video": "/yt/video?url=YOUTUBE_URL",
            "mp3": "/yt/mp3?url=YOUTUBE_URL"
        }
    }

# -----------------------
# Video download endpoint
# -----------------------
@app.get("/yt/video")
def download_video(url: str = Query(...)):
    try:
        url = urllib.parse.unquote(url)
        file_id = str(uuid.uuid4())
        file_path = f"{VIDEO_DIR}/{file_id}.mp4"

        # yt-dlp download
        subprocess.run(["yt-dlp", "-f", "mp4", "-o", file_path, url], check=True)

        return FileResponse(
            path=file_path,
            media_type="video/mp4",
            filename="video.mp4"
        )
    except Exception as e:
        return JSONResponse({"status": False, "error": str(e), "developer": DEVELOPER, "contact": CONTACT})

# -----------------------
# MP3 download endpoint
# -----------------------
@app.get("/yt/mp3")
def download_mp3(url: str = Query(...)):
    try:
        url = urllib.parse.unquote(url)
        file_id = str(uuid.uuid4())
        file_path = f"{MP3_DIR}/{file_id}.mp3"

        # yt-dlp download mp3
        subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "-o", file_path, url], check=True)

        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename="audio.mp3"
        )
    except Exception as e:
        return JSONResponse({"status": False, "error": str(e), "developer": DEVELOPER, "contact": CONTACT})
