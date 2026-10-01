```python
import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
from streamlit_drawable_canvas import st_canvas

Expert = " "
profile_imgenh = " "

# Inicializar session_state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'full_response' not in st.session_state:
    st.session_state.full_response = ""
if 'base64_image' not in st.session_state:
    st.session_state.base64_image = ""


def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(
                image_file.read()
            ).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."


# Streamlit
st.set_page_config(page_title='Tablero Inteligente')
st.title('Tablero Inteligente')

with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader(
        "En esta aplicación veremos la capacidad que ahora tiene "
        "una máquina de interpretar un boceto"
    )

    # Personalización del tablero
    st.subheader("🎨 Personaliza tu tablero")

    # Tamaño del tablero
    canvas_width = st.slider(
        "Ancho del tablero",
        min_value=300,
        max_value=1000,
        value=400,
        step=50
    )

    canvas_height = st.slider(
        "Alto del tablero",
        min_value=200,
        max_value=700,
        value=300,
        step=50
    )

    # Color del tablero
    bg_color = st.color_picker(
        "Color del tablero",
        "#FFFFFF"
    )

    # Color del trazo
    stroke_color = st.color_picker(
        "Color del trazo",
        "#000000"
    )

    # Tamaño del trazo
    stroke_width = st
