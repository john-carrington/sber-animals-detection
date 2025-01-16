import zipfile
from zipfile import ZipFile
from pathlib import Path

from fastapi.responses import FileResponse
from src.app.config import PROCESSED_DIR
from src.app.models.model import process_image

import os


async def process_zip(file, min_confidence, max_objects):
    zip_path = Path("uploads") / file.filename
    with open(zip_path, "wb") as buffer:
        buffer.write(await file.read())

    zip_results = []
    with ZipFile(zip_path, "r") as input_zip:
        for image_path in input_zip.namelist():
            input_zip.extract(image_path, "uploads")
            image_result = process_image(
                Path("uploads") / image_path, min_confidence, max_objects)
            zip_results.append(image_result)

    return zip_results


async def process_video(VIDEO_PATH: str, STEP_SECONDS: int, OUTPUT_PATH: str, ZIP_PATH: str):
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH, exist_ok=True)
    output_file: str = os.path.splitext(os.path.basename(VIDEO_PATH))[0]
    os.system(
        f'ffmpeg -i "{VIDEO_PATH}" -vf "fps=1/{STEP_SECONDS}" -qscale:v 4 "{OUTPUT_PATH}/{output_file}_%03d.jpg"'
    )

    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(OUTPUT_PATH):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, OUTPUT_PATH))

    return {"file_path": ZIP_PATH}
