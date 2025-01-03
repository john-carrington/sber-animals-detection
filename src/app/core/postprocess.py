def process_predictions(predictions):
    """
    Обработка предсказаний модели.
    """
    boxes = predictions["boxes"].tolist()
    labels = predictions["labels"].tolist()
    scores = predictions["scores"].tolist()

    # Фильтруем по порогу уверенности
    threshold = 0.5
    filtered_boxes = [
        (box, label, score)
        for box, label, score in zip(boxes, labels, scores)
        if score > threshold
    ]

    return {
        "boxes": [item[0] for item in filtered_boxes],
        "classes": [item[1] for item in filtered_boxes],
        "scores": [item[2] for item in filtered_boxes]
    }
