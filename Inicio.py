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

    # Color del fondo
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
    stroke_width = st.slider(
        "Tamaño del trazo",
        min_value=1,
        max_value=30,
        value=5,
        step=1
    )


st.subheader(
    "Dibuja el boceto en el panel y presiona el botón para analizarla"
)


# Add canvas component
drawing_mode = "freedraw"

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key="canvas",
)


ke = st.text_input(
    'Ingresa tu Clave',
    type="password"
)

os.environ['OPENAI_API_KEY'] = ke

# Retrieve the OpenAI API Key
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

analyze_button = st.button(
    "Analiza la imagen",
    type="secondary"
)


# Check if an image has been uploaded, if the API key is available,
# and if the button has been pressed
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):

        # Encode the image
        input_numpy_array = np.array(canvas_result.image_data)

        input_image = Image.fromarray(
            input_numpy_array.astype('uint8')
        ).convert('RGBA')

        input_image.save('img.png')

        #
