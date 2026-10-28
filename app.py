import streamlit as st
from src.config import configurar_pagina
from src.ui_components import renderizar_configuracion_principal, renderizar_footer
from src.ai_client import obtener_cliente_gemini, generar_propuesta_cenas
from src.pdf_generator import generar_pdf_menu

# 1. Configuración inicial
configurar_pagina()

st.title("🍲 Asistente de Cenas Familiares")
st.write("Planifica una única cena común, saludable y equilibrada para toda la familia cruzando los menús del mediodía.")

st.markdown("---")

# 2. Configuración persistente en el cuerpo de la app
num_ninos, edades_ninos, fecha_inicio, fecha_fin, tiene_thermomix = renderizar_configuracion_principal()

st.markdown("---")

# 3. Cliente de IA y Subida de Menús
client = obtener_cliente_gemini()

if not client:
    st.error("⚠️ No se ha encontrado la GEMINI_API_KEY en los secretos o variables de entorno.")
else:
    st.subheader("📂 3. Subida de Menús de Mediodía")
    uploaded_files = st.file_uploader(
        f"Sube los {num_ninos} menú(s) en PDF o foto:",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"¡{len(uploaded_files)} archivo(s) cargado(s) correctamente!")

        if st.button("✨ Generar Propuesta de Cenas", type="primary", use_container_width=True):
            with st.spinner("Analizando menús y verificando recetas paso a paso..."):
                try:
                    menu_resultado = generar_propuesta_cenas(
                        client, edades_ninos, fecha_inicio, fecha_fin, tiene_thermomix, uploaded_files
                    )
                    st.session_state.ultimo_menu = menu_resultado
                    st.session_state.fechas_ultimo_menu = (str(fecha_inicio), str(fecha_fin))
                    st.session_state.tm_ultimo_menu = tiene_thermomix
                except Exception as e:
                    st.error(f"Ocurrió un error al procesar con Gemini: {e}")

    # Mostramos el menú generado y su botón de descarga en PDF
    if "ultimo_menu" in st.session_state and st.session_state.ultimo_menu:
        f_ini, f_fin = st.session_state.fechas_ultimo_menu
        tm_usado = st.session_state.tm_ultimo_menu

        st.markdown("---")
        titulo_seccion = f"🍽️ Propuesta de Cenas con Thermomix ({f_ini} al {f_fin})" if tm_usado else f"🍽️ Propuesta de Cenas ({f_ini} al {f_fin})"
        st.subheader(titulo_seccion)

        try:
            pdf_bytes = generar_pdf_menu(st.session_state.ultimo_menu, f_ini, f_fin, tm_usado)
            nombre_archivo = f"Cenas_{f_ini}_al_{f_fin}.pdf"
            st.download_button(
                label=f"📥 Descargar Menú en PDF ({f_ini} al {f_fin})",
                data=pdf_bytes,
                file_name=nombre_archivo,
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"No se pudo preparar la descarga en PDF: {e}")

        st.markdown(st.session_state.ultimo_menu)

# 4. Pie de página con aviso de privacidad y copyright
renderizar_footer()