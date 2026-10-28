import streamlit as st
import datetime
import urllib.parse
import json
from streamlit_local_storage import LocalStorage

def renderizar_configuracion_principal():
    localS = LocalStorage()

    st.markdown("### ⚙️ 1. Configuración Familiar")
    st.caption("Tus datos familiares se guardan automáticamente en este dispositivo.")

    # 1. Inicializamos session_state una sola vez leyendo del navegador
    if "config_cargada" not in st.session_state:
        saved_num = localS.getItem("cfg_num_ninos")
        saved_edades = localS.getItem("cfg_edades_ninos")
        saved_tm = localS.getItem("cfg_thermomix")

        st.session_state.num_ninos = int(saved_num) if saved_num is not None else 2

        if saved_edades:
            try:
                st.session_state.edades_ninos = json.loads(saved_edades) if isinstance(saved_edades, str) else saved_edades
            except Exception:
                st.session_state.edades_ninos = [3.0, 6.0]
        else:
            st.session_state.edades_ninos = [3.0, 6.0]

        st.session_state.tiene_thermomix = (str(saved_tm).lower() == "true") if saved_tm is not None else False

        if saved_num is not None or saved_edades is not None or saved_tm is not None:
            st.session_state.config_cargada = True

    if "guardar_pendiente" not in st.session_state:
        st.session_state.guardar_pendiente = False

    def activar_guardado():
        st.session_state.guardar_pendiente = True
        st.session_state.config_cargada = True

    # 1. Número de comensales / menús
    num_ninos = st.number_input(
        "Número de comensales / menús de mediodía a cruzar:",
        min_value=1,
        max_value=6,
        value=int(st.session_state.num_ninos),
        step=1,
        on_change=activar_guardado
    )
    st.session_state.num_ninos = num_ninos

    # 2. Edades dinámicas
    while len(st.session_state.edades_ninos) < num_ninos:
        st.session_state.edades_ninos.append(5.0)

    edades_ninos = []
    cols_edades = st.columns(min(int(num_ninos), 3))
    for i in range(int(num_ninos)):
        col_actual = cols_edades[i % 3]
        with col_actual:
            edad = st.number_input(
                f"Edad persona {i+1} (años):",
                min_value=0.5,
                max_value=99.0,
                value=float(st.session_state.edades_ninos[i]),
                step=0.5,
                key=f"edad_persona_{i}",
                on_change=activar_guardado
            )
            edades_ninos.append(edad)

    st.session_state.edades_ninos = edades_ninos

    st.markdown("---")
    st.markdown("### 📅 2. Fechas y Cocina")

    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha de inicio:", datetime.date.today())
    with col2:
        fecha_fin = st.date_input("Fecha de fin:", datetime.date.today() + datetime.timedelta(days=6))

    tiene_thermomix = st.checkbox(
        "🍳 ¿Tenemos Thermomix en casa?",
        value=st.session_state.tiene_thermomix,
        help="Si lo marcas, buscará la receta exacta en Cookidoo. Si no existe en Cookidoo, te dará la receta tradicional.",
        on_change=activar_guardado
    )
    st.session_state.tiene_thermomix = tiene_thermomix

    # Solo escribimos en LocalStorage cuando el usuario ha editado la configuración
    if st.session_state.guardar_pendiente:
        localS.setItem("cfg_num_ninos", str(num_ninos), key="save_num")
        localS.setItem("cfg_edades_ninos", json.dumps(edades_ninos), key="save_edades")
        localS.setItem("cfg_thermomix", str(tiene_thermomix), key="save_tm")
        st.session_state.guardar_pendiente = False

    # Buzón de Feedback
    with st.expander("💬 ¿Qué te ha parecido el asistente? Déjanos tu opinión"):
        with st.form("form_feedback"):
            comentario = st.text_area("Escribe tu sugerencia u opinión:")
            email_usuario = st.text_input("Tu email (opcional):")
            enviar_feedback = st.form_submit_button("Enviar Opinión por Email")

            if enviar_feedback:
                if comentario.strip():
                    mi_correo = "TU_CORREO_DE_GMAIL_AQUÍ@gmail.com"
                    asunto = "Feedback sobre el Asistente de Cenas"
                    cuerpo = f"Comentario:\n{comentario}\n\nEnviado por: {email_usuario if email_usuario else 'Anónimo'}"
                    mailto_url = f"mailto:{mi_correo}?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"

                    st.markdown(f"""
                        <div style="margin-top: 10px;">
                            <a href="{mailto_url}" target="_blank" style="background-color: #ff4b4b; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; font-weight: bold; display: inline-block;">
                                ✉️ Pincha aquí para completar el envío por correo
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
                    st.success("¡Pulsa el botón rojo de arriba para enviar el correo!")
                else:
                    st.warning("Por favor, escribe algún comentario.")

    return num_ninos, edades_ninos, fecha_inicio, fecha_fin, tiene_thermomix


def renderizar_footer():
    anio_actual = datetime.date.today().year
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 0.85rem; opacity: 0.75; padding: 10px 0px 20px 0px;">
            <p style="margin-bottom: 5px;">
                🔒 <strong>Privacidad garantizada:</strong> Los archivos subidos y los datos introducidos se procesan en tiempo real y <strong>no se almacenan en ningún servidor</strong> tras su uso. Tu configuración familiar se guarda únicamente en el navegador de tu propio dispositivo.
            </p>
            <p style="margin: 0;">
                © {anio_actual} <strong>Menús a Medida</strong> — Todos los derechos reservados.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )