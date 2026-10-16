import streamlit as st
import datetime
import urllib.parse

def renderizar_sidebar():
    st.sidebar.header("⚙️ Configuración Familiar")
    
    num_ninos = st.sidebar.number_input("Número de niños / menús escolares:", min_value=1, max_value=5, value=2, step=1)
    
    edades_ninos = []
    for i in range(int(num_ninos)):
        edad = st.sidebar.number_input(f"Edad del niño/a {i+1} (años):", min_value=0.5, max_value=18.0, value=3.0, step=0.5)
        edades_ninos.append(edad)

    st.sidebar.markdown("---")
    st.sidebar.header("📅 Rango de Fechas")
    fecha_inicio = st.sidebar.date_input("Fecha de inicio:", datetime.date.today())
    fecha_fin = st.sidebar.date_input("Fecha de fin:", datetime.date.today() + datetime.timedelta(days=6))

    st.sidebar.markdown("---")
    st.sidebar.header("🍳 Preferencias de Cocina")
    tiene_thermomix = st.sidebar.checkbox("¿Tenemos Thermomix?", value=False)

    # Feedback
    st.sidebar.markdown("---")
    st.sidebar.header("💬 ¿Qué te ha parecido?")
    with st.sidebar.form("form_feedback"):
        comentario = st.text_area("Déjanos tu opinión o sugerencia:")
        email_usuario = st.text_input("Tu email (opcional):")
        enviar_feedback = st.form_submit_button("Enviar Opinión por Email")
        
        if enviar_feedback:
            if comentario.strip():
                mi_correo = "TU_CORREO_DE_GMAIL_AQUÍ@gmail.com"
                asunto = "Feedback sobre el Asistente de Cenas"
                cuerpo = f"Comentario:\n{comentario}\n\nEnviado por: {email_usuario if email_usuario else 'Anónimo'}"
                mailto_url = f"mailto:{mi_correo}?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
                
                st.sidebar.markdown(f"""
                    <div style="margin-top: 10px;">
                        <a href="{mailto_url}" target="_blank" style="background-color: #ff4b4b; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; font-weight: bold; display: inline-block;">
                            ✉️ Pincha para enviar por correo
                        </a>
                    </div>
                """, unsafe_allow_html=True)
                st.sidebar.success("¡Pulsa el botón de arriba para completar el envío!")
            else:
                st.sidebar.warning("Por favor, escribe algún comentario.")

    return num_ninos, edades_ninos, fecha_inicio, fecha_fin, tiene_thermomix