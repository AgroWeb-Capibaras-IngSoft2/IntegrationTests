#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Reportes PDF para Tests de AgroWeb
Utiliza ReportLab para crear reportes profesionales
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.platypus.flowables import HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
except ImportError:
    print("❌ Error: ReportLab no está instalado.")
    print("💡 Instala con: pip install reportlab")
    sys.exit(1)

def generate_pdf_report():
    """Genera el reporte PDF usando ReportLab"""
    try:
        # Verificar si existe el archivo de resultados JSON
        results_path = Path(__file__).parent / 'test-results' / 'test-results.json'
        
        if not results_path.exists():
            print('❌ No se encontraron resultados de tests. Ejecuta los tests primero.')
            return False

        # Leer los resultados
        with open(results_path, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Crear archivo PDF
        pdf_path = Path(__file__).parent / 'test-results' / 'test-report-reportlab.pdf'
        
        print('📄 Generando reporte PDF con ReportLab...')
        
        # Crear documento
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Generar contenido
        story = []
        story = add_header(story, results)
        story = add_summary(story, results)
        story = add_test_details(story, results)
        story = add_footer(story)
        
        # Construir PDF
        doc.build(story)
        
        print(f'✅ Reporte PDF generado exitosamente: {pdf_path}')
        return True
        
    except Exception as error:
        print(f'❌ Error generando reporte PDF: {error}')
        return False

def add_header(story, results):
    """Agrega el encabezado del reporte"""
    styles = getSampleStyleSheet()
    
    # Verificar si existe la imagen del escudo institucional
    image_path = Path(__file__).parent / 'escudo_institucional.jpeg'
    
    if image_path.exists():
        # Agregar escudo institucional al encabezado
        try:
            # Crear imagen con tamaño apropiado para el escudo
            img = Image(str(image_path))
            img.drawHeight = 2*inch
            img.drawWidth = 2*inch
            
            # Crear tabla para centrar la imagen
            image_table = Table([[img]], colWidths=[2*inch])
            image_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(image_table)
            story.append(Spacer(1, 20))
        except Exception as e:
            print(f"⚠️ No se pudo cargar el escudo institucional: {e}")
            print("📝 Para agregar el escudo, guarda la imagen como 'escudo_institucional.jpeg'")
    else:
        print("📝 Escudo institucional no encontrado. Guarda la imagen como 'escudo_institucional.jpeg'")
    
    # Título principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2E7D32')
    )
    
    story.append(Paragraph("🧪 REPORTE DE TESTS - AGROWEB", title_style))
    
    # Subtítulo con fecha
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666')
    )
    
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    story.append(Paragraph(f"Generado el: {current_time}", subtitle_style))
    
    # Línea separadora
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4CAF50')))
    story.append(Spacer(1, 20))
    
    return story

def add_summary(story, results):
    """Agrega el resumen de resultados"""
    styles = getSampleStyleSheet()
    
    # Calcular estadísticas
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    total_duration = 0
    
    for suite in results.get('suites', []):
        for sub_suite in suite.get('suites', []):
            for spec in sub_suite.get('specs', []):
                total_tests += 1
                test_passed = all(test.get('status') == 'expected' for test in spec.get('tests', []))
                if test_passed:
                    passed_tests += 1
                else:
                    failed_tests += 1
                
                # Sumar duración
                for test in spec.get('tests', []):
                    for result in test.get('results', []):
                        total_duration += result.get('duration', 0)
    
    success_rate = round((passed_tests / total_tests) * 100, 1) if total_tests > 0 else 0
    duration_seconds = round(total_duration / 1000, 2)
    
    # Título de resumen
    summary_title = ParagraphStyle(
        'SummaryTitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=15,
        textColor=colors.HexColor('#1976D2')
    )
    story.append(Paragraph("📊 RESUMEN EJECUTIVO", summary_title))
    
    # Tabla de resumen
    summary_data = [
        ['📈 Métrica', '🔢 Valor', '📋 Descripción'],
        ['Total de Tests', str(total_tests), 'Número total de casos de prueba ejecutados'],
        ['Tests Exitosos', str(passed_tests), 'Casos de prueba que pasaron correctamente'],
        ['Tests Fallidos', str(failed_tests), 'Casos de prueba que fallaron'],
        ['Tasa de Éxito', f'{success_rate}%', 'Porcentaje de éxito de las pruebas'],
        ['Duración Total', f'{duration_seconds}s', 'Tiempo total de ejecución de todos los tests'],
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 30))
    
    return story

def add_test_details(story, results):
    """Agrega los detalles de cada test"""
    styles = getSampleStyleSheet()
    
    # Título de detalles
    details_title = ParagraphStyle(
        'DetailsTitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=15,
        textColor=colors.HexColor('#388E3C')
    )
    story.append(Paragraph("🔍 DETALLES DE TESTS", details_title))
    
    for suite in results.get('suites', []):
        for sub_suite in suite.get('suites', []):
            # Título del suite
            suite_title = ParagraphStyle(
                'SuiteTitle',
                parent=styles['Heading3'],
                fontSize=14,
                spaceAfter=10,
                textColor=colors.HexColor('#2E7D32')
            )
            story.append(Paragraph(f"📋 {sub_suite.get('title', 'Suite Sin Título')}", suite_title))
            
            # Detalles de cada spec
            for spec in sub_suite.get('specs', []):
                test_data = []
                test_data.append(['🧪 Test', '📊 Estado', '⏱️ Duración', '📝 Detalles'])
                
                for test in spec.get('tests', []):
                    status = "✅ EXITOSO" if test.get('status') == 'expected' else "❌ FALLIDO"
                    duration = 0
                    error_msg = "Sin errores"
                    
                    for result in test.get('results', []):
                        duration += result.get('duration', 0)
                        if result.get('errors'):
                            error_msg = str(result['errors'][0]) if result['errors'] else "Error desconocido"
                    
                    duration_text = f"{round(duration/1000, 2)}s"
                    
                    test_data.append([
                        spec.get('title', 'Test Sin Título'),
                        status,
                        duration_text,
                        error_msg[:50] + "..." if len(error_msg) > 50 else error_msg
                    ])
                
                # Crear tabla de test
                test_table = Table(test_data, colWidths=[2.5*inch, 1*inch, 0.8*inch, 2.2*inch])
                test_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F5E8')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                
                story.append(test_table)
                story.append(Spacer(1, 15))
                
                # Mostrar stdout si existe
                for test in spec.get('tests', []):
                    for result in test.get('results', []):
                        stdout_messages = result.get('stdout', [])
                        if stdout_messages:
                            story.append(Paragraph("📤 Salida del Test:", styles['Heading4']))
                            for msg in stdout_messages:
                                story.append(Paragraph(f"• {msg.get('text', '').strip()}", styles['Normal']))
                            story.append(Spacer(1, 10))
    
    return story

def add_footer(story):
    """Agrega el pie de página"""
    styles = getSampleStyleSheet()
    
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CCCCCC')))
    story.append(Spacer(1, 15))
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666')
    )
    
    story.append(Paragraph("🌱 AgroWeb - Sistema de Testing Automatizado", footer_style))
    story.append(Paragraph("Generado con Playwright + ReportLab", footer_style))
    
    return story

if __name__ == "__main__":
    success = generate_pdf_report()
    sys.exit(0 if success else 1)
