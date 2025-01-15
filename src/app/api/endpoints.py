from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from src.app.models.model import process_image
from src.app.core.preprocess import process_zip
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


@router.get("/get_image/{image_name}")
async def get_image(image_name: str):
    return FileResponse(PROCESSED_DIR / image_name)
