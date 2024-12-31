from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from io import BytesIO
import zipfile
import os
import cv2
from roboflow import Roboflow
import shutil
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

rf = Roboflow(api_key="h4Ebts2tdf2CFEG741ri")
project = rf.workspace().project("deers-07-12")
model = project.version(1).model

app = FastAPI()

IMAGES_DIR = "docs"

os.makedirs(IMAGES_DIR, exist_ok=True)


def process_image(image_path, output_path):
    logger.info(f"Processing image: {image_path}")
    image = Image.open(image_path).convert('RGB')
    image.save(output_path)
    result = model.predict(output_path, confidence=40, overlap=50)
    result.save(output_path)
    logger.info(f"Processed image saved: {output_path}")


def process_zip(zip_file, output_zip_path):
    logger.info(f"Processing ZIP file: {zip_file}")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(IMAGES_DIR)

    processed_images = []
    for file_name in os.listdir(IMAGES_DIR):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(IMAGES_DIR, file_name)
            output_path = os.path.join(IMAGES_DIR, f"processed_{file_name}")
            process_image(input_path, output_path)
            processed_images.append(output_path)
            os.remove(input_path)

    if not processed_images:
        logger.error("No images found in the ZIP file for processing.")
        raise HTTPException(
            status_code=400, detail="No images found in the ZIP file for processing.")

    with zipfile.ZipFile(output_zip_path, 'w') as zip_ref:
        for file in processed_images:
            zip_ref.write(file, os.path.basename(file))
            os.remove(file)

    logger.info(f"Processed ZIP file created: {output_zip_path}")


@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(IMAGES_DIR, file.filename)
    output_path = os.path.join(IMAGES_DIR, "output.jpg")
    output_zip_path = os.path.join(IMAGES_DIR, "output.zip")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        process_image(file_path, output_path)
        os.remove(file_path)

        with open(output_path, "rb") as f:
            image_data = f.read()

        os.remove(output_path)
        return StreamingResponse(BytesIO(image_data), media_type="image/jpeg")
    elif file.filename.lower().endswith('.zip'):
        process_zip(file_path, output_zip_path)
        os.remove(file_path)
        return FileResponse(output_zip_path, media_type="application/zip", filename="output.zip")
    else:
        logger.error(f"Unsupported file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Unsupported file type")


@app.get("/get_summarisation")
async def get_summarisation():
    logger.info("Endpoint /get_summarisation called")
    return {"message": "This endpoint is not yet implemented."}


@app.get("/get_box_count")
async def get_count():
    logger.info("Endpoint /get_count called")
    return {"message": "This endpoint is not yet implemented."}


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")
    shutil.rmtree(IMAGES_DIR)
