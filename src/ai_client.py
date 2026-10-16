import streamlit as st
from google import genai
from google.genai import types

def obtener_cliente_gemini():
    try:
        gemini_api_key = st.secrets["GEMINI_API_KEY"]
        return genai.Client(api_key=gemini_api_key)
    except Exception:
        return None

def generar_propuesta_cenas(client, edades_ninos, fecha_inicio, fecha_fin, tiene_thermomix, uploaded_files):
    edades_str = ", ".join([f"{e} años" for e in edades_ninos])
    
    prompt = (
        f"Actúa como un nutricionista infantil experto. "
        f"Tienes la obligación estricta y absoluta de UTILIZAR TODOS LOS MENÚS ESCOLARES ADJUNTOS "
        f"para analizar qué han comido al mediodía los niños (con edades de: {edades_str}, sin alergias conocidas). "
        f"El objetivo es diseñar una propuesta de cenas equilibrada y conjunta para el periodo comprendido entre el {fecha_inicio} y el {fecha_fin}. "
        f"Cruza la información de todos los menús escolares día a día para que la cena compense y complemente exactamente lo que todos los niños han comido al mediodía de forma simultánea. "
        f"Alterna verdura, hidratos (patata/cereal), proteína magra (pescado blanco, carne blanca o huevo) y fruta de postre según los huecos nutricionales de cada jornada."
    )

    if tiene_thermomix:
        prompt += (
            " ADEMÁS, dado que la familia cuenta con Thermomix, incluye para cada cena recomendada los títulos de recetas iguales o muy similares "
            "que se puedan buscar y encontrar fácilmente en la plataforma oficial de recetas Cookidoo."
        )

    contents = [prompt]
    
    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.getvalue()
        if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
            contents.append(
                types.Part.from_bytes(data=file_bytes, mime_type=uploaded_file.type)
            )
        elif uploaded_file.type == "application/pdf":
            contents.append(
                types.Part.from_bytes(data=file_bytes, mime_type="application/pdf")
            )

    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=contents,
    )
    return response.text