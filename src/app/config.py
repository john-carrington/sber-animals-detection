from pathlib import Path
from ultralytics import YOLO

MODEL_PATH: str = 'best.pt'
UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)
