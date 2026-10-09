import streamlit as st
from google import genai
from google.genai import types
import datetime

# Configuración de la página
st.set_page_config(page_title="Asistente de Cenas Infantiles", page_icon="🍲", layout="centered")

# --- ESTILOS ADAPTATIVOS PARA MODO CLARO Y OSCURO ---
st.markdown("""
    <style>
    @media (prefers-color-scheme: dark) {
        .stMarkdown, p, li, span, h1, h2, h3 {
            color: #f3f4f6 !important;
        }
        div.stMarkdown div {
            color: #f3f4f6;
        }
    }
    @media (prefers-color-scheme: light) {
        .stMarkdown, p, li, span {
            color: #1f2937 !important;
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

st.title("🍲 Asistente de Cenas Familiares")
st.write("Configura los datos de los niños y las fechas para generar un plan de cenas equilibrado y adaptado.")

# --- BARRA LATERAL DE CONFIGURACIÓN (Multi-familia) ---
st.sidebar.header("⚙️ Configuración Familiar")

# 1. Número de menús / niños a tener en cuenta
num_ninos = st.sidebar.number_input("Número de niños / menús escolares:", min_value=1, max_value=5, value=2, step=1)

# 2. Edades de los niños de forma dinámica
edades_ninos = []
for i in range(int(num_ninos)):
    edad = st.sidebar.number_input(f"Edad del niño/a {i+1} (años):", min_value=0.5, max_value=18.0, value=3.0, step=0.5)
    edades_ninos.append(edad)

st.sidebar.markdown("---")

# 3. Selección de fechas para la planificación
st.sidebar.header("📅 Rango de Fechas")
fecha_inicio = st.sidebar.date_input("Fecha de inicio:", datetime.date.today())
fecha_fin = st.sidebar.date_input("Fecha de fin:", datetime.date.today() + datetime.timedelta(days=6))

# --- CARGA AUTOMÁTICA DE LA GEMINI_API_KEY DESDE LOS SECRETOS ---
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    gemini_api_key = None

if not gemini_api_key:
    st.error("⚠️ No se ha encontrado la GEMINI_API_KEY en los secretos de Streamlit. Por favor, configúrala en el panel de Streamlit Cloud.")
else:
    client = genai.Client(api_key=gemini_api_key)

    # 4. Subida de menús escolares adaptada al número de niños
    st.subheader("📂 Subida de Menús Escolares")
    uploaded_files = st.file_uploader(
        f"Sube los {num_ninos} menú(s) escolar(es) (PDFs o fotos):", 
        type=["pdf", "png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"¡{len(uploaded_files)} archivo(s) cargado(s) correctamente!")

        if st.button("Generar Propuesta de Cenas"):
            with st.spinner("Gemini está cruzando los menús y planificando las cenas..."):
                
                # Construcción dinámica del prompt con la información personalizada
                edades_str = ", ".join([f"{e} años" for e in edades_ninos])
                prompt = (
                    f"Actúa como un nutricionista infantil experto. "
                    f"Tienes la obligación estricta y absoluta de UTILIZAR TODOS LOS MENÚS ESCOLARES ADJUNTOS "
                    f"para analizar qué han comido al mediodía los niños (con edades de: {edades_str}, sin alergias conocidas). "
                    f"El objetivo es diseñar una propuesta de cenas equilibrada y conjunta para el periodo comprendido entre el {fecha_inicio} y el {fecha_fin}. "
                    f"Cruza la información de todos los menús escolares día a día para que la cena compense y complemente exactamente lo que todos los niños han comido al mediodía de forma simultánea. "
                    f"Alterna verdura, hidratos (patata/cereal), proteína magra (pescado blanco, carne blanca o huevo) y fruta de postre según los huecos nutricionales de cada jornada."
                )

                contents = [prompt]
                
                # Adjuntamos los archivos subidos
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
                    # Actualizado al modelo recomendado actual
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=contents,
                    )
                    
                    menu_resultado = response.text
                    
                    st.subheader(f"✨ Propuesta de Cenas ({fecha_inicio} al {fecha_fin})")
                    st.markdown(menu_resultado)

                except Exception as e:
                    st.error(f"Ocurrió un error al procesar con Gemini: {e}")