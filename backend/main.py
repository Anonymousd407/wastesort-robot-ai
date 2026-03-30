import os
import base64
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import load_dotenv
from PIL import Image
import io

# Load .env
load_dotenv()

app = FastAPI()

# CORS for frontend (React/JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OXLO_API_KEY = os.getenv("OXLO_API_KEY")
BASE_URL = "https://api.oxlo.ai/v1"

# Supported image types
ALLOWED_TYPES = {"jpeg", "png", "gif", "bmp", "webp"}

# Max image size in bytes after resize
MAX_BYTES = 2 * 1024 * 1024  # 2 MB

@app.get("/")
def root():
    return {"message": "WasteSort AI Backend Running"}

@app.post("/analyze-multiple")
async def analyze_multiple(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    results = []

    for f in files:
        contents = await f.read()
        if len(contents) == 0:
            results.append({"file": f.filename, "error": "Empty file"})
            continue

        # Validate image and resize if needed
        try:
            img = Image.open(io.BytesIO(contents))
            img_format = img.format

            # Resize large images
            MAX_DIM = 1024
            img.thumbnail((MAX_DIM, MAX_DIM))

            buffer = io.BytesIO()
            img.save(buffer, format=img_format, quality=85)
            contents = buffer.getvalue()

            if len(contents) > MAX_BYTES:
                results.append({"file": f.filename, "error": "File too large after resize"})
                continue

        except Exception:
            results.append({"file": f.filename, "error": "Unsupported or broken image"})
            continue

        # Encode to base64
        image_b64 = base64.b64encode(contents).decode("utf-8")

        detect_body = {
            "model": "yolo11x.pt",
            "image": image_b64,
        }

        # Call Oxlo API
        try:
            resp = requests.post(
                f"{BASE_URL}/detect",
                headers={
                    "Authorization": f"Bearer {OXLO_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=detect_body,
                timeout=30
            )
            if resp.status_code != 200:
                results.append({"file": f.filename, "error": f"API Error: {resp.status_code}"})
                continue

            response_json = resp.json()
            item_type = "Unknown"
            if "detections" in response_json and len(response_json["detections"]) > 0:
                item_type = response_json["detections"][0].get("class_name", "Unknown")

            # Placeholder extra info
            age_estimate = "Unknown"
            hazard = "No hazard info."
            recycle_method = "Follow local recycling rules."
            solution = "Handle according to waste type."

            results.append({
                "file": f.filename,
                "type": item_type,
                "age": age_estimate,
                "hazard": hazard,
                "recycle_method": recycle_method,
                "solution": solution
            })

        except requests.exceptions.RequestException as e:
            results.append({"file": f.filename, "error": f"Request failed: {str(e)}"})

    return results
