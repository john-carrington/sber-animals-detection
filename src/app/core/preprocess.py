from zipfile import ZipFile
from pathlib import Path
from src.app.models.model import process_image


async def process_zip(file, min_confidence, min_size, max_objects):
    zip_path = Path("uploads") / file.filename
    with open(zip_path, "wb") as buffer:
        buffer.write(await file.read())

    zip_results = []
    with ZipFile(zip_path, "r") as input_zip:
        for image_path in input_zip.namelist():
            input_zip.extract(image_path, "uploads")
            image_result = process_image(
                Path("uploads") / image_path, min_confidence, min_size, max_objects)
            zip_results.append(image_result)

    return zip_results
