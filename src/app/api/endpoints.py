from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from src.app.core.preprocess import preprocess_image, extract_images_from_zip
from src.app.core.postprocess import process_predictions
from src.app.core.visualization import draw_predictions
from src.app.models.model import predict_with_mask_rcnn
from PIL import Image
import io
import zipfile
import os
import shutil
from typing import List

router = APIRouter()

UPLOAD_FOLDER = "./temp/uploads"
PROCESSED_FOLDER = "./temp/processed"

# Создание временных папок для обработки
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


@router.post("/upload/")
async def upload_images(files: List[UploadFile] = File(...)):
    """
    Загрузка изображений (одного, нескольких или ZIP-архива) для обработки.
    """
    results = []
    try:
        for file in files:
            if file.filename.endswith(".zip"):
                # Извлечение изображений из ZIP-архива
                extracted_files = await extract_images_from_zip(file, UPLOAD_FOLDER)
                results.extend(extracted_files)
            else:
                # Сохранение обычных изображений
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                with open(file_path, "wb") as f:
                    f.write(await file.read())
                results.append(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка загрузки: {str(e)}")

    return {"uploaded_files": results}


@router.post("/predict/")
async def predict_images(files: List[UploadFile] = File(...)):
    """
    Выполнение предсказаний для загруженных изображений.
    """
    predictions = []
    for file in files:
        # Преобразование изображения
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
        preprocessed_image = preprocess_image(image)

        # Предсказания модели
        predictions_dict = predict_with_mask_rcnn(preprocessed_image)

        # Постобработка результатов
        processed_predictions = process_predictions(predictions_dict)

        # Визуализация
        processed_image = draw_predictions(image, processed_predictions)

        # Сохранение визуализированного изображения
        processed_path = os.path.join(PROCESSED_FOLDER, file.filename)
        processed_image.save(processed_path)

        predictions.append({
            "file_name": file.filename,
            "classes": processed_predictions["classes"],
            "num_boxes": len(processed_predictions["boxes"]),
            "processed_image": processed_path
        })

    return {"predictions": predictions}


@router.get("/processed/{file_name}")
def get_processed_image(file_name: str):
    """
    Получение обработанного изображения с боксами.
    """
    file_path = os.path.join(PROCESSED_FOLDER, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    return FileResponse(file_path)
