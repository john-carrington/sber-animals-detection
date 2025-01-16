import gradio as gr
import requests as r

from PIL import Image
from pathlib import Path


def create_pdf():
    pass


def create_table():
    pass


def predict(images, minConvidence=0.25, maxObjects=300):
    result = []
    object_list = []
    headers = {
        'accept': 'application/json'}

    data = {
        'minConfidence': minConvidence,
        'maxObjects': maxObjects
    }

    for idx, image in enumerate(images):
        files = {'file': open(image, 'rb'), 'type': 'image/png'}
        response = r.post('http://127.0.0.1:8000/predict',
                          headers=headers, data=data, files=files).json()
        processed_files = response['results']

        for processed_file in processed_files:
            result.append(Image.open(Path('processed') /
                          processed_file['img_name']))
            if processed_file['count_boxes'] != 0:
                class_names = [result['class_name']
                               for result in processed_file['results']]
                unique_classes = {class_name: class_names.count(
                    class_name) for class_name in set(class_names)}
                object_list.append({
                    'Номер фотографии': idx + 1,
                    'Количество животных': processed_file['count_boxes'],
                    'Название найденных животных': unique_classes
                })
            else:
                object_list.append({
                    'Номер фотографии': idx + 1,
                    'Попробуйте загрузить другое изображение': 'На фотографии животных не найдено'
                })

    # Формирование презентабельного вывода
    output = "## Результаты распознавания:\n\n"
    for obj in object_list:
        if 'Количество животных' in obj:
            output += f" | Заголовок | Сведения |\n"
            output += f"| ---      | ---       |\n"
            output += f"| **Номер фотографии** | {obj['Номер фотографии']} |\n"
            output += f"| **Количество животных** | {obj['Количество животных']} |\n"
            output += "| **Найденные животные** |"
            for class_name, count in obj['Название найденных животных'].items():
                output += f"{class_name} "
            output += "| \n"

            for class_name, count in obj['Название найденных животных'].items():
                output += f"    - {class_name}: {count}\n"
            output += "\n\n"
    return result, gr.Markdown(output)


gallery = gr.Gallery(
    label="Generated images", show_label=False, elem_id="gallery", columns=[1], object_fit="contain", height="auto")

data = gr.Markdown()

predict_page = gr.Interface(
    predict,
    inputs=[gr.File(
        file_count='multiple',
        file_types=['image', '.zip']), gr.Text(0.25), gr.Text(300)],
    outputs=[gallery, data],
)
