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
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
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

    # -----------------------------------
    # TAMAÑO DEL TABLERO
    # -----------------------------------
    st.markdown("### 📐 Tamaño del tablero")

    canvas_width = st.slider(
        "Ancho",
        min_value=300,
        max_value=1000,
        value=400,
        step=50
    )

    canvas_height = st.slider(
        "Alto",
        min_value=200,
        max_value=700,
        value=300,
        step=50
    )

    # -----------------------------------
    # COLOR DEL TABLERO
    # -----------------------------------
    st.markdown("### 🖼️ Color del tablero")

    bg_color = st.color_picker(
        "Selecciona el color del fondo",
        "#FFFFFF"
    )

    # -----------------------------------
    # COLOR DEL TRAZO
    # -----------------------------------
    st.markdown("### 🖊️ Color del trazo")

    stroke_color = st.color_picker(
        "Selecciona el color del trazo",
        "#000000"
    )

    # -----------------------------------
    # TAMAÑO DEL TRAZO
    # -----------------------------------
    st.markdown("### 📏 Tamaño del trazo")

    stroke_width = st.slider(
        "Selecciona el ancho de línea",
        min_value=1,
        max_value=30,
        value=5,
        step=1
    )


st.subheader("Dibuja el boceto en el panel y presiona el botón para analizarlo")


# -----------------------------------
# BOTÓN PARA LIMPIAR EL TABLERO
# -----------------------------------

if st.button("🧹 Limpiar tablero"):
    st.rerun()


# -----------------------------------
# CANVAS
# -----------------------------------

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


# -----------------------------------
# API KEY
# -----------------------------------

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


# -----------------------------------
# ANALIZAR IMAGEN
# -----------------------------------

if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):

        # Encode the image
        input_numpy_array = np.array(canvas_result.image_data)

        input_image = Image.fromarray(
            input_numpy_array.astype('uint8')
        ).convert('RGBA')

        input_image.save('img.png')

        # Codificar la imagen en base64
        base64_image = encode_image_to_base64("img.png")

        st.session_state.base64_image = base64_image

        prompt_text = (
            f"Describe in spanish briefly the image"
        )

        # Make the request to the OpenAI API
        try:

            full_response = ""
            message_placeholder = st.empty()

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt_text
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )

            if response.choices[0].message.content is not None:

                full_response += response.choices[0].message.content

                message_placeholder.markdown(
                    full_response + "▌"
                )

            # Final update to placeholder after the stream ends
            message_placeholder.markdown(full_response)

            # Guardar en session_state
            st.session_state.full_response = full_response
            st.session_state.analysis_done = True

            if Expert == profile_imgenh:
                st.session_state.mi_respuesta = (
                    response.choices[0].message.content
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")


# -----------------------------------
# CREAR HISTORIA
# -----------------------------------

if st.session_state.analysis_done:

    st.divider()

    st.subheader("📚 ¿Quieres crear una historia?")

    if st.button("✨ Crear historia infantil"):

        with st.spinner("Creando historia..."):

            story_prompt = (
                f"Basándote en esta descripción: "
                f"'{st.session_state.full_response}', "
                f"crea una historia infantil breve y entretenida. "
                f"La historia debe ser creativa y apropiada para niños."
            )

            story_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": story_prompt
                    }
                ],
                max_tokens=500,
            )

            st.markdown("**📖 Tu historia:**")

            st.write(
                story_response.choices[0].message.content
            )


# -----------------------------------
# WARNING
# -----------------------------------

if not api_key:

    st.warning(
        "Por favor ingresa tu API key."
    )
```
