from pathlib import Path
import cv2
import uuid
from ultralytics import YOLO


def process_image(image_path: Path, min_confidence, min_size, max_objects) -> dict:
    model = YOLO("best.pt")
    results = model(image_path)

    if not results[0].boxes:
        print("No detections found.")
        return None

    image = cv2.imread(str(image_path))

    results_to_send = {
        'img': '',
        'results': []
    }

    objects_count = 0

    for box in results[0].boxes:
        if objects_count > max_objects:
            break
        objects_count += 1

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = box.conf[0]
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        label = f"{model.names[class_id]} {confidence:.2f}"
        width = x2 - x1
        height = y2 - y1
        size = (width ** 2 + height ** 2) ** 0.5

        skip = confidence < min_confidence or size < min_size
        if skip:
            continue

        results_to_send['results'].append(
            {'class_name': class_name, 'size': f'{size:.2f}', 'confidence': f'{confidence:.2f}'})
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    processed_dir = Path("processed")
    processed_dir.mkdir(exist_ok=True)
    image_name = f"processed_{uuid.uuid4().hex}.jpg"
    processed_image_path = processed_dir / image_name

    results_to_send['img'] = image_name

    cv2.imwrite(str(processed_image_path), image)
    print(f"Saved processed image to: {processed_image_path}")

    return results_to_send
