import streamlit as st
import datetime
import urllib.parse

def renderizar_configuracion_principal():
    st.markdown("### ⚙️ 1. Configuración Familiar")
    st.write("Configura los datos de los niños y las fechas. Se guardarán en este dispositivo para futuras visitas.")
    
    # Usamos session_state para mantener los valores en la sesión activa del navegador
    if "num_ninos" not in st.session_state:
        st.session_state.num_ninos = 2
    if "edades_ninos" not in st.session_state:
        st.session_state.edades_ninos = [3.0, 6.0]

    num_ninos = st.number_input(
        "Número de niños / menús escolares:", 
        min_value=1, 
        max_value=5, 
        value=st.session_state.num_ninos, 
        step=1,
        key="input_num_ninos"
    )
    st.session_state.num_ninos = num_ninos

    edades_ninos = []
    # Aseguramos que la lista tenga la longitud correcta
    while len(st.session_state.edades_ninos) < num_ninos:
        st.session_state.edades_ninos.append(3.0)

    for i in range(int(num_ninos)):
        edad = st.number_input(
            f"Edad del niño/a {i+1} (años):", 
            min_value=0.5, 
            max_value=18.0, 
            value=float(st.session_state.edades_ninos[i]), 
            step=0.5,
            key=f"edad_nino_{i}"
        )
        edades_ninos.append(edad)
    st.session_state.edades_ninos = edades_ninos

    st.markdown("---")
    st.markdown("### 📅 2. Rango de Fechas y Preferencias")
    
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha de inicio:", datetime.date.today())
    with col2:
        fecha_fin = st.date_input("Fecha de fin:", datetime.date.today() + datetime.timedelta(days=6))

    tiene_thermomix = st.checkbox("🍳 ¿Tenemos Thermomix en casa?", value=False, help="Marca esta opción si quieres sugerencias de Cookidoo.")

    # Feedback situado de forma accesible al final de la página principal o secundaria
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
                    st.success("¡Pulsa el botón de arriba para abrir tu correo!")
                else:
                    st.warning("Por favor, escribe algún comentario.")

    return num_ninos, edades_ninos, fecha_inicio, fecha_fin, tiene_thermomix