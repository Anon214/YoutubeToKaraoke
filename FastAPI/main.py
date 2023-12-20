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
    allow_origins=["http://localhost:3000"],
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
        'outtmpl': 'FastAPI/audio',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])


def separate_vocals(input_file):
    command = [
        'spleeter',
        'separate',
        '-p', 'spleeter:2stems',
        '-b', '320k',
        '-o', "./FastAPI",
        input_file
    ]

    subprocess.run(command, check=True, shell=True)

@app.post("/process_link")
async def process_link(data: dict):
    try:
        audio_path = "FastAPI/audio"
        if os.path.exists(audio_path):
            shutil.rmtree(audio_path)

        youtube_url = text = data.get("url")

        if text is None:
            raise HTTPException(status_code=400, detail="No URL submitted")
        
        download_youtube_audio(youtube_url)
        separate_vocals("FastAPI/audio.mp3")

        return  FileResponse('FastAPI/audio/accompaniment.wav', media_type="audio/wav", filename="accompaniment.wav")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)