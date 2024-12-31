import streamlit as st
from pages.md_description import PageDescription

st.set_page_config(
    page_title="Главная страница",
    page_icon="👁",
)

st.sidebar.success("Выберите раздел выше")

st.markdown(PageDescription.main_page)
