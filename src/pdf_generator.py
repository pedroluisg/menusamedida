from fpdf import FPDF
import re

def limpiar_texto_para_pdf(texto):
    # Reemplazamos caracteres especiales habituales que no están en latin-1
    reemplazos = {
        "•": "-",
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "€": "EUR"
    }
    for orig, dest in reemplazos.items():
        texto = texto.replace(orig, dest)

    # Eliminamos marcas de formato Markdown
    texto = texto.replace("**", "").replace("##", "").replace("###", "").replace("`", "")
    
    # Filtramos emojis manteniendo todos los caracteres del español (latin-1)
    texto_limpio = re.sub(r'[^\x00-\xff]', '', texto)
    return texto_limpio

def generar_pdf_menu(texto_menu, fecha_inicio, fecha_fin, tiene_thermomix):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(left=15, top=15, right=15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Ancho efectivo de escritura (210mm ancho A4 - 30mm de márgenes = 180mm)
    ancho_util = pdf.epw

    # Título principal del documento
    pdf.set_font("Helvetica", "B", 15)
    titulo = f"Propuesta de Cenas ({fecha_inicio} al {fecha_fin})"
    titulo_seguro = titulo.encode('latin-1', 'replace').decode('latin-1')
    pdf.set_x(15)
    pdf.multi_cell(ancho_util, 9, titulo_seguro, align="C")

    # Subtítulo indicando la modalidad
    pdf.set_font("Helvetica", "I", 10)
    subtitulo = "Modalidad: Con recetas de Thermomix (Cookidoo) / Tradicional" if tiene_thermomix else "Modalidad: Cocina Tradicional"
    subtitulo_seguro = subtitulo.encode('latin-1', 'replace').decode('latin-1')
    pdf.set_x(15)
    pdf.multi_cell(ancho_util, 7, subtitulo_seguro, align="C")
    pdf.ln(3)

    # Línea separadora
    pdf.set_draw_color(200, 200, 200)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(5)

    # Cuerpo del menú con las recetas
    texto_procesado = limpiar_texto_para_pdf(texto_menu)
    dias_semana = ["lunes", "martes", "miércoles", "miercoles", "jueves", "viernes", "sábado", "sabado", "domingo"]

    for linea in texto_procesado.split('\n'):
        linea_limpia = linea.strip()
        
        # Ignoramos líneas vacías o separadores de guiones
        if not linea_limpia or set(linea_limpia) <= {"-", "_", "*", "="}:
            pdf.ln(2)
            continue

        linea_segura = linea_limpia.encode('latin-1', 'replace').decode('latin-1')

        # Volvemos siempre al margen izquierdo antes de escribir
        pdf.set_x(15)

        # Si la línea es el encabezado de un día, la destacamos en negrita
        if any(dia in linea_segura.lower() for dia in dias_semana) and len(linea_segura) < 95:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 12)
            pdf.multi_cell(ancho_util, 7, linea_segura, align="L", wrapmode="CHAR")
            pdf.set_font("Helvetica", "", 10)
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(ancho_util, 5.5, linea_segura, align="L", wrapmode="CHAR")

    return bytes(pdf.output())