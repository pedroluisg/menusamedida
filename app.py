import streamlit as st
from src.config import configurar_pagina
from src.ui_components import renderizar_sidebar
from src.ai_client import obtener_cliente_gemini, generar_propuesta_cenas

# 1. Configuración inicial
configurar_pagina()

st.title("🍲 Asistente de Cenas Familiares")
st.write("Configura los datos de los niños, las fechas y tus preferencias para generar un plan de cenas equilibrado.")

# 2. Sidebar y parámetros
num_ninos, edades_ninos, fecha_inicio, fecha_fin, tiene_thermomix = renderizar_sidebar()

# 3. Cliente de IA
client = obtener_cliente_gemini()

if not client:
    st.error("⚠️ No se ha encontrado la GEMINI_API_KEY en los secretos de Streamlit.")
else:
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
                try:
                    menu_resultado = generar_propuesta_cenas(
                        client, edades_ninos, fecha_inicio, fecha_fin, tiene_thermomix, uploaded_files
                    )
                    
                    titulo_seccion = f"✨ Propuesta de Cenas con Thermomix ({fecha_inicio} al {fecha_fin})" if tiene_thermomix else f"✨ Propuesta de Cenas ({fecha_inicio} al {fecha_fin})"
                    st.subheader(titulo_seccion)
                    st.markdown(menu_resultado)

                except Exception as e:
                    st.error(f"Ocurrió un error al procesar con Gemini: {e}")