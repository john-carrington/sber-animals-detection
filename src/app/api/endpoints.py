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
import base64

router = APIRouter()


@router.post("/predict/")
async def predict_images(files: List[UploadFile] = File(...)):
    """
    Выполнение предсказаний для загруженных изображений и возврат обработанного изображения.
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

        # Сохранение визуализированного изображения в буфер памяти
        img_byte_arr = io.BytesIO()
        # Выберите формат по необходимости
        processed_image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        # Кодирование изображения в Base64
        base64_image = base64.b64encode(img_byte_arr).decode('utf-8')

        predictions.append({
            "file_name": file.filename,
            "num_boxes": len(processed_predictions["boxes"]),
            "processed_image_base64": base64_image
        })

    return predictions
