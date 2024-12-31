# from ultralytics import RTDETR

# model = RTDETR("rtdetr-l.pt")

# model.info()

# results = model.train(data="coco8.yaml", epochs=2, imgsz=640)

# results = model("test.jpg")

from ultralytics import YOLO


class ModelDetect(YOLO):
    def get_count_boxes(self, result) -> int:
        return len(result[0].boxes.xyxy.tolist())
