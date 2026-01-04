from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import subprocess, uuid, os

router = APIRouter(prefix="/yt")

BASE_DIR = "downloads"
VIDEO_DIR = f"{BASE_DIR}/video"
AUDIO_DIR = f"{BASE_DIR}/audio"

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)


def run_cmd(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"yt-dlp failed: {str(e)}"
        )


@router.get("/video")
def download_video(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Missing url")

    file_id = str(uuid.uuid4())
    output = f"{VIDEO_DIR}/{file_id}.mp4"

    cmd = [
        "yt-dlp",
        "-f", "bv*+ba/b",
        "--merge-output-format", "mp4",
        "--no-playlist",
        "-o", output,
        url
    ]

    run_cmd(cmd)

    return FileResponse(
        path=output,
        filename="video.mp4",
        media_type="video/mp4"
    )


@router.get("/mp3")
def download_mp3(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Missing url")

    file_id = str(uuid.uuid4())
    output = f"{AUDIO_DIR}/{file_id}.mp3"

    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--no-playlist",
        "-o", output,
        url
    ]

    run_cmd(cmd)

    return FileResponse(
        path=output,
        filename="audio.mp3",
        media_type="audio/mpeg"
    )
