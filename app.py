import streamlit as __st__
from openai import OpenAI

# Configuración de la página
__st__.set_page_config(
    page_title="Asistente de Cenas Infantiles", page_icon="🍲", layout="centered"
)

# Estilo visual moderno y amable con CSS personalizado
__st__.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #ff6b6b;
        color: white;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff5252;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabecera amigable
__st__.title("✨ Tu Asistente Inteligente de Cenas")
__st__.write(
    "Sube los menús del colegio o guardería de tus hijos (2 y 4 años) y genera automáticamente las cenas equilibradas para toda la semana sin repetir ingredientes."
)

# Panel lateral para configuración de la API y datos de los niños
with __st__.sidebar:
    __st__.header("⚙️ Configuración")
    api_key = __st__.text_input("Introduce tu OpenAI API Key", type="password")

    __st__.markdown("---")
    __st__.subheader("👶 Perfil de los peques")
    __st__.text("Edades: 2 y 4 años")
    __st__.text("Alergias: Ninguna conocida")

# Área principal: Subir archivos
__st__.markdown("### 📂 Sube los menús de la semana")
uploaded_files = __st__.file_uploader(
    "Puedes subir fotos o PDFs (ej. Menú comedor y Purés)",
    type=["png", "jpg", "jpeg", "pdf"],
    accept_multiple_files=True,
)

# Selector de semana
semana = __st__.text_input(
    "¿Para qué semana es el menú?", "Del 13 al 16 de octubre de 2026"
)

if __st__.button("🚀 Generar Planificador de Cenas"):
  if not api_key:
    __st__.error("Por favor, introduce tu API Key de OpenAI en la barra lateral.")
  elif not uploaded_files:
    __st__.warning("Por favor, sube al menos un menú o archivo.")
  else:
    with __st__.spinner(
        "Analizando menús y equilibrando nutrientes para los peques..."
    ):
      # Aquí conectarías con el cliente de IA para procesar las imágenes/PDFs y aplicar el prompt del sistema
      client = OpenAI(api_key=api_key)

      prompt_sistema = (
          "Eres un asistente nutricional experto en alimentación infantil (niños de 2 y 4 años). "
          "A partir de los menús de mediodía proporcionados en las imágenes/archivos, diseña un menú de cenas "
          "para la semana indicada que complemente perfectamente lo que ya han comido al mediodía, "
          "siguiendo la pauta: verdura + hidrato (patata/cereal) + proteína magra (pescado blanco, carne blanca o huevo) + fruta."
      )

      # Simulación de respuesta generada por la IA estructurada con tarjetas
      __st__.success("¡Menú de cenas generado con éxito!")

      __st__.markdown(
          f"### 🍽️ Propuesta de Cenas ({semana})", unsafe_allow_html=True
      )

      # Ejemplo visual de la estructura que devolvería la IA
      dias = [
          (
              "Martes, 13",
              "Crema suave de calabacín y patata",
              "Pescado blanco a la plancha",
              "Fruta fresca",
          ),
          (
              "Miércoles, 14",
              "Sopa de verduras con fideos",
              "Pechuga de pollo tierna",
              "Fruta fresca",
          ),
          (
              "Jueves, 15",
              "Puré ligero de zanahoria",
              "Tortilla francesa suave",
              "Yogur natural",
          ),
          (
              "Viernes, 16",
              "Crema de calabaza",
              "Merluza desmenuzada al horno",
              "Fruta fresca",
          ),
      ]

      for dia, plato1, plato2, postre in dias:
        __st__.markdown(
            f"""
                <div class="card">
                    <h4>📅 {dia}</h4>
                    <ul>
                        <li><b>Primer plato:</b> {plato1}</li>
                        <li><b>Segundo plato:</b> {plato2}</li>
                        <li><b>Postre:</b> {postre}</li>
                    </ul>
                </div>
            """,
            unsafe_allow_html=True,
        )