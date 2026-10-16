from fpdf import FPDF
import re

def limpiar_texto_para_pdf(texto):
    # Eliminamos el formato de negritas y encabezados de Markdown para que quede limpio
    texto = texto.replace("**", "").replace("##", "").replace("###", "")
    # Filtramos emojis e iconos manteniendo todos los caracteres del español (tildes, ñ, ¡, ¿, º, ª)
    texto_limpio = re.sub(r'[^\x00-\xff]', '', texto)
    return texto_limpio

def generar_pdf_menu(texto_menu, fecha_inicio, fecha_fin, tiene_thermomix):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título principal del documento
    pdf.set_font("Helvetica", "B", 16)
    titulo = f"Propuesta de Cenas ({fecha_inicio} al {fecha_fin})"
    pdf.cell(0, 10, titulo.encode('latin-1', 'replace').decode('latin-1'), ln=True, align="C")

    # Subtítulo indicando la modalidad
    pdf.set_font("Helvetica", "I", 11)
    subtitulo = "Modalidad: Con recetas de Thermomix (Cookidoo) / Tradicional" if tiene_thermomix else "Modalidad: Cocina Tradicional"
    pdf.cell(0, 8, subtitulo.encode('latin-1', 'replace').decode('latin-1'), ln=True, align="C")
    pdf.ln(5)

    # Línea separadora
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # Cuerpo del menú con las recetas
    pdf.set_font("Helvetica", "", 10)
    texto_procesado = limpiar_texto_para_pdf(texto_menu)

    for linea in texto_procesado.split('\n'):
        linea_limpia = linea.strip()
        if not linea_limpia:
            pdf.ln(3)
            continue

        # Si la línea es el encabezado de un día, la destacamos en negrita
        if any(dia in linea_limpia.lower() for dia in ["lunes", "martes", "miércoles", "miercoles", "jueves", "viernes", "sábado", "sabado", "domingo"]) and len(linea_limpia) < 85:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 12)
            linea_segura = linea_limpia.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 7, linea_segura)
            pdf.set_font("Helvetica", "", 10)
        else:
            linea_segura = linea_limpia.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 5.5, linea_segura)

    return bytes(pdf.output())