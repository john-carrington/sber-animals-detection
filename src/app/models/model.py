import torch
import torch.nn as nn
from torchvision.models.detection import maskrcnn_resnet50_fpn_v2, MaskRCNN_ResNet50_FPN_V2_Weights

# Загрузка модели
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = maskrcnn_resnet50_fpn_v2(
    pretrained=True, weights=MaskRCNN_ResNet50_FPN_V2_Weights.COCO_V1)
model.eval()
model.to(device)


def predict_with_mask_rcnn(image_tensor):
    """
    Выполнение предсказаний с помощью Mask R-CNN.
    """
    with torch.no_grad():
        predictions = model([image_tensor.to(device)])
    return predictions[0]
