import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import ImageDraw


def draw_predictions(image, predictions):
    """
    Наложение боксов и классов на изображение.
    """
    draw = ImageDraw.Draw(image)
    for box, label, score in zip(predictions["boxes"], predictions["classes"], predictions["scores"]):
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        draw.text((x1, y1), f"{label}: {score:.2f}", fill="red")
    return image
