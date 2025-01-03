import torch
from torchvision.models.detection import maskrcnn_resnet50_fpn

# Загрузка модели
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = maskrcnn_resnet50_fpn(pretrained=True)
model.eval()
model.to(device)


def predict_with_mask_rcnn(image_tensor):
    """
    Выполнение предсказаний с помощью Mask R-CNN.
    """
    with torch.no_grad():
        predictions = model([image_tensor.to(device)])
    return predictions[0]
