from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from typing import Dict, Any, Optional
import io

def generar_pdf_diagnostico(diagnostico: Dict[str, Any], hechos: Dict[str, bool]) -> bytes:
    """
    Genera un PDF con el diagnóstico ambiental
    
    Args:
        diagnostico: Diccionario con el resultado del diagnóstico
        hechos: Diccionario con los hechos observados
    
    Returns:
        Bytes del PDF generado
    """
    # Crear buffer en memoria
    buffer = io.BytesIO()
    
    # Crear documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Contenedor para los elementos del PDF
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulos
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    # Estilo para el nivel de riesgo
    riesgo_style = ParagraphStyle(
        'RiesgoStyle',
        parent=styles['Normal'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # ===== ENCABEZADO =====
    story.append(Paragraph("SISTEMA EXPERTO AMBIENTAL", titulo_style))
    story.append(Paragraph("Diagnóstico Ambiental Urbano", styles['Heading3']))
    story.append(Spacer(1, 0.3*inch))
    
    # Fecha del diagnóstico
    fecha_actual = datetime.now().strftime("%d de %B de %Y - %H:%M")
    story.append(Paragraph(f"<b>Fecha del Diagnóstico:</b> {fecha_actual}", normal_style))
    
    if diagnostico.get('diagnostico_id'):
        story.append(Paragraph(f"<b>ID del Diagnóstico:</b> #{diagnostico['diagnostico_id']}", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # ===== NIVEL DE RIESGO =====
    riesgo = diagnostico.get('riesgo', 'DESCONOCIDO')
    color_riesgo = colors.HexColor('#e74c3c') if riesgo == 'ALTO' else \
                   colors.HexColor('#f39c12') if riesgo == 'MEDIO' else \
                   colors.HexColor('#27ae60')
    
    riesgo_text = f'<font color="{color_riesgo.hexval()}">NIVEL DE RIESGO: {riesgo}</font>'
    story.append(Paragraph(riesgo_text, riesgo_style))
    story.append(Spacer(1, 0.2*inch))
    
    # ===== INFORMACIÓN DEL DIAGNÓSTICO =====
    story.append(Paragraph("INFORMACIÓN DEL DIAGNÓSTICO", subtitulo_style))
    
    # Título del problema
    titulo_problema = diagnostico.get('titulo', 'Sin título')
    story.append(Paragraph(f"<b>Problema Identificado:</b> {titulo_problema}", normal_style))
    
    # Categoría
    categoria = diagnostico.get('categoria', 'Sin categoría')
    story.append(Paragraph(f"<b>Categoría:</b> {categoria}", normal_style))
    
    # Descripción
    descripcion = diagnostico.get('descripcion', 'Sin descripción')
    story.append(Paragraph(f"<b>Descripción:</b> {descripcion}", normal_style))
    
    # Justificación
    justificacion = diagnostico.get('justificacion', 'Sin justificación')
    story.append(Paragraph(f"<b>Justificación Técnica:</b> {justificacion}", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # ===== ACCIONES RECOMENDADAS =====
    story.append(Paragraph("ACCIONES RECOMENDADAS", subtitulo_style))
    
    acciones = diagnostico.get('acciones', [])
    if acciones:
        for i, accion in enumerate(acciones, 1):
            story.append(Paragraph(f"{i}. {accion}", normal_style))
    else:
        story.append(Paragraph("No se especificaron acciones.", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # ===== INDICADORES EVALUADOS =====
    story.append(Paragraph("INDICADORES EVALUADOS", subtitulo_style))
    
    # Crear tabla con los hechos
    indicadores_data = [['Indicador', 'Estado']]
    
    nombres_indicadores = {
        'olor_fuerte': 'Olor fuerte o desagradable',
        'vegetacion_deteriorada': 'Vegetación deteriorada',
        'residuos_acumulados': 'Residuos acumulados',
        'humedad_excesiva': 'Humedad excesiva',
        'ruido_elevado': 'Ruido elevado',
        'aire_contaminado': 'Aire contaminado',
        'agua_turbia': 'Agua turbia'
    }
    
    for hecho_id, valor in hechos.items():
        nombre = nombres_indicadores.get(hecho_id, hecho_id)
        estado = 'SÍ ✓' if valor else 'NO ✗'
        indicadores_data.append([nombre, estado])
    
    # Crear tabla
    tabla = Table(indicadores_data, colWidths=[4*inch, 1.5*inch])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    story.append(tabla)
    story.append(Spacer(1, 0.3*inch))
    
    # ===== PIE DE PÁGINA =====
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("_" * 80, normal_style))
    story.append(Paragraph(
        "<i>Este diagnóstico fue generado automáticamente por el Sistema Experto Ambiental. "
        "Se recomienda validar con inspecciones in situ y consultar con especialistas en gestión ambiental.</i>",
        ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_JUSTIFY,
            fontName='Helvetica-Oblique'
        )
    ))
    
    # Construir PDF
    doc.build(story)
    
    # Obtener bytes del PDF
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def generar_pdf_historial(diagnosticos: list) -> bytes:
    """
    Genera un PDF con el historial de diagnósticos
    
    Args:
        diagnosticos: Lista de diagnósticos
    
    Returns:
        Bytes del PDF generado
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Título
    titulo_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    story.append(Paragraph("HISTORIAL DE DIAGNÓSTICOS AMBIENTALES", titulo_style))
    story.append(Paragraph(f"Total de diagnósticos: {len(diagnosticos)}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Tabla resumen
    data = [['ID', 'Fecha', 'Riesgo', 'Categoría', 'Título']]
    
    for diag in diagnosticos:
        fecha = datetime.fromisoformat(diag['fecha']).strftime("%d/%m/%Y %H:%M") if 'fecha' in diag else 'N/A'
        data.append([
            str(diag.get('id', 'N/A')),
            fecha,
            diag.get('riesgo', 'N/A'),
            diag.get('categoria', 'N/A')[:20] + '...' if len(diag.get('categoria', '')) > 20 else diag.get('categoria', 'N/A'),
            diag.get('titulo', 'N/A')[:30] + '...' if len(diag.get('titulo', '')) > 30 else diag.get('titulo', 'N/A')
        ])
    
    tabla = Table(data, colWidths=[0.5*inch, 1.5*inch, 0.8*inch, 1.5*inch, 2.5*inch])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    
    story.append(tabla)
    
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

