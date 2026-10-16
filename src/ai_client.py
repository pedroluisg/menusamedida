import streamlit as st
import os
from google import genai
from google.genai import types

def obtener_cliente_gemini():
    gemini_api_key = None

    try:
        if "GEMINI_API_KEY" in st.secrets:
            gemini_api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if not gemini_api_key:
        gemini_api_key = os.environ.get("GEMINI_API_KEY")

    if gemini_api_key:
        try:
            return genai.Client(api_key=gemini_api_key)
        except Exception:
            return None

    return None

def generar_propuesta_cenas(client, edades_ninos, fecha_inicio, fecha_fin, tiene_thermomix, uploaded_files):
    num_personas = len(edades_ninos)
    edades_str = ", ".join([f"{e} años" for e in edades_ninos])

    instruccion_cocina = ""
    if tiene_thermomix:
        instruccion_cocina = (
            "REGLA ESTRICTA DE THERMOMIX (COOKIDOO):\n"
            "- La familia TIENE Thermomix. Utiliza obligatoriamente la herramienta de búsqueda de Google para verificar si la receta elegida existe realmente en 'cookidoo.es'.\n"
            "- Si encuentras la receta real en Cookidoo: pon el NOMBRE EXACTO tal como figura en Cookidoo y detalla los pasos resumidos para Thermomix (tiempos, temperatura y velocidad).\n"
            "- Si tras buscar verificas que NO existe una receta igual o muy similar en Cookidoo: PROHIBIDO INVENTARLA. Indica 'Preparación tradicional (no disponible en Cookidoo)' y explica la receta tradicional paso a paso.\n"
        )
    else:
        instruccion_cocina = (
            "REGLA DE COCINA TRADICIONAL:\n"
            "- La familia NO tiene Thermomix. Busca en internet la receta casera más apropiada, saludable y rápida para ese plato y descríbela paso a paso de forma tradicional.\n"
        )

    prompt = (
        f"Actúa como un nutricionista familiar experto y chef práctico.\n"
        f"Analiza TODOS los menús de mediodía adjuntos correspondientes a {num_personas} comensales (edades: {edades_str}) que han comido en sitios separados.\n"
        f"Diseña el plan de cenas desde el {fecha_inicio} hasta el {fecha_fin} cumpliendo estas reglas:\n\n"
        f"1. UNA SOLA CENA COMÚN POR NOCHE: Decide una única cena para todos los comensales cada día (sin dar opciones A/B), que equilibre de la forma más lógica lo que cada uno ha comido a mediodía.\n"
        f"2. RESPUESTA CLARA, CORTA Y DIRECTA: Ve directo al grano sin introducciones ni despedidas.\n"
        f"3. {instruccion_cocina}\n"
        f"4. FORMATO OBLIGATORIO PARA CADA DÍA:\n"
        f"### [Día de la semana y Fecha] - [Nombre del plato único + postre]\n"
        f"- **Lógica nutricional:** (1 frase corta explicando por qué compensa las comidas del mediodía).\n"
        f"- **Modalidad / Receta:** (Nombre exacto verificado en Cookidoo o 'Receta tradicional').\n"
        f"- **Ingredientes ({num_personas} personas):** (Lista concisa en una línea).\n"
        f"- **Preparación paso a paso:** (Pasos cortos, numerados y claros).\n"
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

    # Activamos Google Search para que verifique en vivo Cookidoo y recetas reales
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.2,
            )
        )
    except Exception:
        # Respaldo automático en caso de que la red de búsqueda sufra un corte puntual
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=contents,
        )

    return response.text