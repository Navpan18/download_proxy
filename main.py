from fastapi import FastAPI, HTTPException , Request
from fastapi.responses import FileResponse
import requests
import os
import random
from datetime import datetime
import string

app = FastAPI()
def generate_random_string(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def generate_video_name():
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = generate_random_string()
    return f"video_{current_datetime}_{random_string}.mp4"

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/upload/")
async def read_item(url: str,request: Request):
    try:
        # Download the video from the provided URL
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to download video")

        # Save the video on the server
        video_file_path = generate_video_name()  # Replace with your desired server path
        with open(video_file_path, "wb") as video_file:
            video_file.write(response.content)

        server_url = str(request.base_url)
        return {"video_url": f"{server_url}get?file_path={video_file_path}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get/")
async def get_video(file_path: str):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    down = generate_video_name()
    # Send the file in the response
    response = FileResponse(file_path, media_type="video/mp4", filename=down)

    # Delete the file after sending it

    return response
@app.get("/del/")
async def delete_video(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": "Video deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Video not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))