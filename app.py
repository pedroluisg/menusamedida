import streamlit as st
import base64
from openai import OpenAI

# Configuración de la página
st.set_page_config(page_title="Asistente de Cenas Infantiles", page_icon="🍲", layout="centered")

# --- CORRECCIÓN VISUAL DE LOS TEXTOS Y CAJAS ---
st.markdown("""
    <style>
    .stMarkdown, p, li, span {
        color: #1f2937 !important;
    }
    h1, h2, h3 {
        color: #111827 !important;
    }
    div.stMarkdown div {
        color: #1f2937;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍲 Asistente de Cenas para los Peques")
st.write("Sube los menús del comedor de ambos niños para generar propuestas de cena equilibradas, cruzando toda la información para adaptarlas a los dos al mismo tiempo.")

# --- CARGA AUTOMÁTICA DE LA API KEY DESDE LOS SECRETOS DE STREAMLIT ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("⚠️ No se ha encontrado la OPENAI_API_KEY en los secretos de Streamlit. Por favor, configúrala en el panel de Streamlit Cloud.")
else:
    client = OpenAI(api_key=api_key)

    # Subida de archivos (permite varios menús a la vez)
    uploaded_files = st.file_uploader(
        "Sube los menús escolares (pueden ser varios archivos o fotos):", 
        type=["pdf", "png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"¡{len(uploaded_files)} archivo(s) cargado(s) correctamente!")

        if st.button("Generar Menú de Cenas Semanal"):
            with st.spinner("Analizando todos los menús y cruzando datos nutricionales para ambos niños..."):
                
                prompt = (
                    "Actúa como un nutricionista infantil experto. "
                    "Tienes la obligación estricta y absoluta de UTILIZAR TODOS LOS MENÚS ESCOLARES ADJUNTOS para analizar qué han comido al mediodía. "
                    "El objetivo es diseñar una propuesta de cenas semanales equilibrada y conjunta para dos niños de 2 y 4 años (sin alergias) "
                    "que se adecue, complemente y compense lo que ambos han comido al mediodía de forma simultánea. "
                    "Alterna verdura, hidratos (patata/cereal), proteína magra (pescado blanco, carne blanca o huevo) y fruta de postre según lo que haya faltado en el conjunto de los menús."
                )

                messages_content = [{"type": "text", "text": prompt}]
                
                for uploaded_file in uploaded_files:
                    file_bytes = uploaded_file.getvalue()
                    
                    if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
                        base64_image = base64.b64encode(file_bytes).decode("utf-8")
                        messages_content.append({
                            "type": "image_url",
                            "image_url": {"url": f"data:{uploaded_file.type};base64,{base64_image}"}
                        })

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o", 
                        messages=[{"role": "user", "content": messages_content}],
                        max_tokens=1500
                    )
                    
                    menu_resultado = response.choices[0].message.content
                    
                    st.subheader("✨ Propuesta de Cenas Equilibradas")
                    st.markdown(menu_resultado)

                except Exception as e:
                    st.error(f"Ocurrió un error al procesar con OpenAI: {e}")