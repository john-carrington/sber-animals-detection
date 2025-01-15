# import gradio as gr
import gradio as gr
from predict_model_page import *


def main() -> None:
    demo = gr.TabbedInterface(

        [predict_page],  # Вкладки
        ["Анализ изображений"]  # Названия вкладок
    )

    demo.launch()


if __name__ == '__main__':
    main()
