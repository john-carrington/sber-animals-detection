from PIL import Image
from torchvision import transforms
import zipfile
import os
import io


def preprocess_image(image):
    """
    Преобразование изображения для передачи в модель.
    """
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    return transform(image)


async def extract_images_from_zip(zip_file, output_folder):
    """
    Извлечение изображений из ZIP-архива.
    """
    if not zipfile.is_zipfile(zip_file.file):
        raise ValueError("Файл не является ZIP-архивом")

    zip_file.file.seek(0)
    with zipfile.ZipFile(io.BytesIO(await zip_file.read())) as zf:
        extracted_files = []
        for file_name in zf.namelist():
            if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                extracted_path = os.path.join(output_folder, file_name)
                with zf.open(file_name) as f:
                    with open(extracted_path, "wb") as out_file:
                        out_file.write(f.read())
                extracted_files.append(extracted_path)
    return extracted_files
