# import gradio as gr
import gradio as gr
from predict_model_page import *
from video_cut_page import video_cut


def main() -> None:
    demo = gr.TabbedInterface(

        [predict_page, video_cut],  # Вкладки
        ["Анализ изображений", 'Раскадровка видео']  # Названия вкладок
    )

    demo.launch()


if __name__ == '__main__':
    main()
