import os
import uuid
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from src.app.models.model import process_image
from src.app.core.preprocess import process_video, process_zip
from src.app.config import *

router = APIRouter()


@router.post("/predict")
async def upload_file(file: UploadFile = File(...), minConfidence: float = Form(...), maxObjects: int = Form(...)):
    if file.filename.endswith('.zip'):

        results = await process_zip(file, minConfidence, maxObjects)
        if results:
            return {"results": results}
        else:
            raise HTTPException(status_code=200, detail="Nothing found")

    else:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        processed_image_path = process_image(
            file_path, minConfidence, maxObjects)

        if processed_image_path:
            return {"results": [processed_image_path]}
        else:
            raise HTTPException(status_code=200, detail="Nothing found")


@router.post("/process_video")
async def cut_video(file: UploadFile = File(...), step_seconds: int = 1):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    zip_filename = f"{os.path.splitext(file.filename)[0]}_frames_{uuid.uuid4().hex}.zip"
    zip_path = PROCESSED_DIR / zip_filename
    output_path = PROCESSED_DIR / \
        f"{os.path.splitext(file.filename)[0]}_frames_{uuid.uuid4().hex}"

    return await process_video(str(file_path), step_seconds, str(output_path), str(zip_path))


@ router.get("/get_image/{image_name}")
async def get_image(image_name: str):
    return FileResponse(PROCESSED_DIR / image_name)
