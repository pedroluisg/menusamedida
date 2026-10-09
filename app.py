import streamlit as st
from google import genai
from google.genai import types

# Configuración de la página
st.set_page_config(page_title="Asistente de Cenas Infantiles", page_icon="🍲", layout="centered")

# --- ESTILOS ADAPTATIVOS PARA MODO CLARO Y OSCURO ---
st.markdown("""
    <style>
    /* Estilos automáticos según el tema del dispositivo (Claro / Oscuro) */
    @media (prefers-color-scheme: dark) {
        .stMarkdown, p, li, span, h1, h2, h3 {
            color: #f3f4f6 !important; /* Texto claro muy legible sobre fondo oscuro */
        }
        div.stMarkdown div {
            color: #f3f4f6;
        }
    }
    @media (prefers-color-scheme: light) {
        .stMarkdown, p, li, span {
            color: #1f2937 !important; /* Texto oscuro sobre fondo claro */
        }
        h1, h2, h3 {
            color: #111827 !important;
        }
        div.stMarkdown div {
            color: #1f2937;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍲 Asistente de Cenas para los Peques")
st.write("Sube los menús del comedor de ambos niños para generar propuestas de cena equilibradas, cruzando toda la información con Gemini.")

# --- CARGA AUTOMÁTICA DE LA GEMINI_API_KEY DESDE LOS SECRETOS ---
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    gemini_api_key = None

if not gemini_api_key:
    st.error("⚠️ No se ha encontrado la GEMINI_API_KEY en los secretos de Streamlit. Por favor, configúrala en el panel de Streamlit Cloud.")
else:
    # Inicializamos el cliente oficial de Google GenAI
    client = genai.Client(api_key=gemini_api_key)

    # Subida de archivos (permite varios menús a la vez)
    uploaded_files = st.file_uploader(
        "Sube los menús escolares (pueden ser PDFs o fotos):", 
        type=["pdf", "png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"¡{len(uploaded_files)} archivo(s) cargado(s) correctamente!")

        if st.button("Generar Menú de Cenas Semanal"):
            with st.spinner("Gemini está analizando todos los menús y cruzando los datos nutricionales..."):
                
                # Prompt estructurado para Gemini
                prompt = (
                    "Actúa como un nutricionista infantil experto. "
                    "Tienes la obligación estricta y absoluta de UTILIZAR TODOS LOS MENÚS ESCOLARES ADJUNTOS para analizar qué han comido al mediodía. "
                    "El objetivo es diseñar una propuesta de cenas semanales equilibrada y conjunta para dos niños de 2 y 4 años (sin alergias) "
                    "que se adecue, complemente y compense lo que ambos han comido al mediodía de forma simultánea. "
                    "Alterna verdura, hidratos (patata/cereal), proteína magra (pescado blanco, carne blanca o huevo) y fruta de postre según lo que haya faltado en el conjunto de los menús."
                )

                contents = [prompt]
                
                # Procesamos cada archivo subido para dárselo a Gemini
                for uploaded_file in uploaded_files:
                    file_bytes = uploaded_file.getvalue()
                    
                    if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
                        contents.append(
                            types.Part.from_bytes(
                                data=file_bytes,
                                mime_type=uploaded_file.type,
                            )
                        )
                    elif uploaded_file.type == "application/pdf":
                        contents.append(
                            types.Part.from_bytes(
                                data=file_bytes,
                                mime_type="application/pdf",
                            )
                        )

                try:
                    # Usamos gemini-2.5-flash para análisis rápido y preciso de imágenes/PDFs
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents,
                    )
                    
                    menu_resultado = response.text
                    
                    st.subheader("✨ Propuesta de Cenas Equilibradas")
                    st.markdown(menu_resultado)

                except Exception as e:
                    st.error(f"Ocurrió un error al procesar con Gemini: {e}")