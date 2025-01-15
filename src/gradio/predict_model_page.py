from pathlib import Path
import gradio as gr
import requests as r

from gradio_image_prompter import ImagePrompter
from PIL import Image

import requests as r


def predict(images):
    result = []
    headers = {
        'accept': 'application/json'}

    data = {
        'minConfidence': '0.25',
        'maxObjects': '100'
    }

    for image in images:
        files = {'file': open(image, 'rb'), 'type': 'image/png'}
        processed_files = r.post('http://127.0.0.1:8000/predict',
                                 headers=headers, data=data, files=files).json()['results']
        for processed_file in processed_files:
            result.append(Image.open(Path('processed') /
                          processed_file['img_name']))

    return result, gr.Markdown(
        """
    # Hello World!
    Start typing below to see the output.
    """)


gallery = gr.Gallery(
    label="Generated images", show_label=False, elem_id="gallery", columns=[1], object_fit="contain", height="auto")

data = gr.Markdown()

predict_page = gr.Interface(
    predict,
    inputs=gr.File(
        file_count='multiple',
        file_types=['image', '.zip']),
    outputs=[gallery, data],


)
