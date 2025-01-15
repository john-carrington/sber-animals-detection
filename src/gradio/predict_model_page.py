import gradio as gr
import requests as r
from gradio_image_prompter import ImagePrompter


def predict(image):

    return image


gallery = gr.Gallery(
    label="Generated images", show_label=False, elem_id="gallery", columns=[1], rows=[10], object_fit="contain", height="auto")

data = gr.Dataframe()

predict_page = gr.Interface(
    inputs=gr.File(
        file_types=['image', '.zip']),
    outputs=[gallery, data],
)
