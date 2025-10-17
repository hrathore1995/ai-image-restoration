import os
import shutil
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from PIL import Image

from .restore import restore_image

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/restore")
async def restore_endpoint(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    original_path = os.path.join(temp_dir, file.filename)
    try:
        with open(original_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    
    try:
        img = Image.open(original_path)

        width, height = img.size
        new_size = min(width, height)
        left = (width - new_size)/2
        top = (height - new_size)/2
        right = (width + new_size)/2
        bottom = (height + new_size)/2
        img_cropped = img.crop((left, top, right, bottom))
        
        img_resized = img_cropped.resize((1024, 1024), Image.Resampling.LANCZOS)

        img_rgba = img_resized.convert("RGBA")

        processed_filename = f"processed_{os.path.splitext(file.filename)[0]}.png"
        processed_path = os.path.join(temp_dir, processed_filename)
        img_rgba.save(processed_path, 'PNG')

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {e}")

    try:
        restored_path, restored_name = restore_image(processed_path)
    except Exception as e:
        print("\n AN EXCEPTION OCCURRED ")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    return FileResponse(restored_path, media_type="image/png", filename=restored_name)