import subprocess
import yt_dlp

from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000, http://localhost:8000, http://localhost:8000/process_link"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_youtube_audio(video_url):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': '/code/audio',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])


def separate_vocals(input_file):
    try:
        command = [
            'spleeter',
            'separate',
            '-p', 'spleeter:2stems',
            '-b', '320k',
            '-o', "./",
            input_file
        ]

        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Error separating vocals: {e}")
        raise

@app.post("/process_link")
async def process_link(data: dict):
    try:
        audio_path = "/code/audio"
        if os.path.exists(audio_path):
            shutil.rmtree(audio_path)
        if os.path.exists("/code/audio.mp3"):
            shutil.rmtree("/code/audio.mp3")

        youtube_url = data.get("url")

        if youtube_url is None:
            raise HTTPException(status_code=400, detail="No URL submitted")
        
        download_youtube_audio(youtube_url)
        separate_vocals("/code/audio.mp3")

        acc_path = '/code/audio/accompaniment.wav'

        if not os.path.exists(acc_path): # docker
            acc_path = '/code/audio/accompaniment.wav'

        return FileResponse(acc_path, media_type="audio/wav", filename="accompaniment.wav")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)