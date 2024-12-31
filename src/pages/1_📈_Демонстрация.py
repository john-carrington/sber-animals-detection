from io import BytesIO
import streamlit as st
import requests
import cv2


from pages.md_description import PageDescription
from models.detect_baseline import ModelDetect
from streamlit_elements import elements, mui, html

from PIL import Image


# infer on a local image

st.markdown(PageDescription.demo_page)


uploaded_file = st.sidebar.file_uploader(
    "Загрузите изображение", type=['png', 'jpeg', 'jpg'])


if uploaded_file is not None:
    is_valid = True
    with st.spinner(text='Загрузка..'):
        st.sidebar.markdown('***Оригинальное изображение***')
        st.sidebar.image(uploaded_file)

    st.image(requests.post(
        'http://127.0.0.1:8000/upload_image', files={'file': uploaded_file}))

    st.markdown('### **Данные с изображения**')

    with elements("style_mui_sx"):
        mui.Box(
            f"Количество: ",
            sx={
                "bgcolor": "background.paper",
                "boxShadow": 1,
                "borderRadius": 2,
                "p": 2,
                "minWidth": 300,
            }
        )

        mui.Box(
            f"Виды млекопитающих: None",
            sx={
                "bgcolor": "background.paper",
                "boxShadow": 1,
                "margin-top": 10,
                "borderRadius": 2,
                "p": 2,
                "minWidth": 300,
            }
        )
else:
    with elements("style_mui_sx"):
        mui.Box(
            "Загрузите изображение",
            sx={
                "bgcolor": "#2a4934",
                "boxShadow": 1,
                "text-align": "center",
                "borderRadius": 2,
                "p": 5,
                "minWidth": 300,
            }
        )
