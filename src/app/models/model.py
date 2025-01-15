import cv2
import uuid
import json
from app.config import MODEL_PATH
from ultralytics import YOLO
from pathlib import Path

model = YOLO(MODEL_PATH)


def process_image(image_path: Path, min_confidence, max_objects) -> dict:
    results = model(image_path, conf=min_confidence, max_det=max_objects)
    image = cv2.imread(str(image_path))

    result_json: json.dump = {
        'img_name': str,
        'count_boxes': int,
        'results': list()
    }

    for result in results:
        result_json['count_boxes'] = len(result.boxes)

        for box in result.boxes:
            x1, y1, x2, y2 = map(lambda x: round(float(x), 2), box.xyxy[0])
            confidence = round(float(box.conf[0]), 2)

            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            label = f"{model.names[class_id]} {confidence:.2f}"

            width = x2 - x1
            height = y2 - y1

            size = round((width ** 2 + height ** 2) ** 0.5, 2)

            result_json['results'].append({
                'class_name': class_name,
                'class_id': class_id,
                'confidence': confidence,
                'coordinates': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2},
                'size': size
            })

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    processed_dir = Path("processed")
    processed_dir.mkdir(exist_ok=True)

    image_name = f"processed_{uuid.uuid4().hex}.jpg"
    result_json['img_name'] = image_name

    processed_image_path = processed_dir / image_name
    cv2.imwrite(str(processed_image_path), image)

    print(f"Saved processed image to: {processed_image_path}")
    return result_json
