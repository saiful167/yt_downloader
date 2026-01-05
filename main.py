from fastapi import FastAPI
from yt_router import router

app = FastAPI(
    title="YouTube Downloader API",
    description="FastAPI + yt-dlp (Render & Android compatible)",
    version="1.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "status": "running",
        "developer": "SAIFUL ISLAM",
        "contact": "Telegram: @saifulmn",
        "endpoints": {
            "video": "/yt/video?url=YOUTUBE_URL",
            "mp3": "/yt/mp3?url=YOUTUBE_URL"
        }
    }
