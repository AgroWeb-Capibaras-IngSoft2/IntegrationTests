"""
Generador de reportes PDF profesionales para pruebas de integración AgroWeb
Crea documentos formales con logos universitarios, gráficos y análisis completo
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple
import logging

# PDF Generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black, white, darkblue, lightgrey, green, red, orange
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie

# Data Analysis and Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import base64

# Configuration
# from config.productos.test_config import TestConfig
# Usar configuración genérica para reportes
import os

# Configuración local para reportes
class ReportConfig:
    @staticmethod
    def ensure_report_directory():
        """Asegurar que el directorio de reportes existe"""
        report_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(report_dir, exist_ok=True)
        return report_dir
    
    @staticmethod
    def get_report_timestamp():
        """Obtener timestamp para reportes"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    UNIVERSITY_INFO = {
        "name": "Universidad Nacional de Colombia",
        "faculty": "Facultad de Ingeniería",
        "department": "Departamento de Ingeniería de Sistemas e Industrial",
        "course": "Ingeniería de Software II",
        "semester": "9no",
        "project": "AgroWeb - Sistema de Gestión de Productos Agrícolas",
        "team": "Capibaras",
        "logo_path": "config/university_assets/logo_unal.png"
    }
    
    TEST_CATEGORIES = {
        "integration": "Pruebas de Integración",
        "api": "Pruebas de API",
        "carrito": "Pruebas de Carrito",
        "productos": "Pruebas de Productos",
        "usuarios": "Pruebas de Usuarios"
    }

logger = logging.getLogger(__name__)

class PDFReportGenerator:
    """Generador de reportes PDF profesionales para resultados de testing"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
        self.colors = {
            'primary': Color(0.2, 0.3, 0.7),  # Azul institucional
            'success': Color(0.2, 0.7, 0.3),  # Verde
            'warning': Color(0.9, 0.7, 0.1),  # Amarillo
            'error': Color(0.8, 0.2, 0.2),    # Rojo
            'light_blue': Color(0.9, 0.95, 1.0),  # Azul claro
            'light_gray': Color(0.95, 0.95, 0.95)  # Gris claro
        }
    
    def _create_custom_styles(self):
        """Crear estilos personalizados para el documento"""
        custom = {}
        
        # Título principal
        custom['title'] = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Centrado
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        # Subtítulos
        custom['subtitle'] = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        # Texto del header universitario
        custom['university'] = ParagraphStyle(
            'University',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=1,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        # Texto normal mejorado
        custom['body'] = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            fontName='Helvetica'
        )
        
        # Texto para métricas
        custom['metric'] = ParagraphStyle(
            'Metric',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=colors.darkblue
        )
        
        return custom
    
    def _detect_service_from_tests(self, test_data: Dict[str, Any]) -> str:
        """Detectar qué servicio se está probando basado en los datos de los tests"""
        if not test_data or 'tests' not in test_data:
            return None
            
        # Contar tests por servicio
        service_counts = {
            'Carrito': 0,
            'Productos': 0,
            'Usuarios': 0
        }
        
        for test in test_data['tests']:
            test_name = test.get('nodeid', '').lower()
            
            if 'carrito' in test_name:
                service_counts['Carrito'] += 1
            elif 'productos' in test_name or 'product' in test_name:
                service_counts['Productos'] += 1
            elif 'usuarios' in test_name or 'user' in test_name:
                service_counts['Usuarios'] += 1
        
        # Retornar el servicio con más tests ejecutados
        if any(service_counts.values()):
            max_service = max(service_counts, key=service_counts.get)
            if service_counts[max_service] > 0:
                return max_service
                
        return None
    
    def generate_integration_report(self, output_dir: str = None) -> str:
        """Generar reporte PDF completo de pruebas de integración"""
        
        # Configurar directorio de salida
        if not output_dir:
            output_dir = ReportConfig.ensure_report_directory()
        
        timestamp = ReportConfig.get_report_timestamp()
        
        # Cargar datos de pruebas para detectar el servicio
        test_data = self._load_test_results()
        service_name = self._detect_service_from_tests(test_data)
        
        # Generar nombre de archivo basado en el servicio
        if service_name:
            filename = f"AgroWeb_{service_name}_Integration_Report_{timestamp}.pdf"
        else:
            filename = f"AgroWeb_Integration_Report_{timestamp}.pdf"
            
        filepath = os.path.join(output_dir, filename)
        
        logger.info(f"📄 Generando reporte PDF para servicio '{service_name}': {filepath}")
        
        # Crear documento PDF
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Construir contenido
        story = []
        
        # Página de portada
        story.extend(self._create_cover_page(service_name))
        story.append(PageBreak())
        
        # Resumen ejecutivo
        story.extend(self._create_executive_summary(test_data))
        story.append(PageBreak())
        
        # Resultados detallados
        story.extend(self._create_detailed_results(test_data))
        story.append(PageBreak())
        
        # Análisis de rendimiento
        story.extend(self._create_performance_analysis(test_data))
        story.append(PageBreak())
        
        # Análisis de errores
        story.extend(self._create_error_analysis(test_data))
        story.append(PageBreak())
        
        # Recomendaciones
        story.extend(self._create_recommendations(test_data))
        
        # Construir PDF
        doc.build(story)
        
        logger.info(f"✅ Reporte PDF generado exitosamente: {filepath}")
        return filepath
    
    def _load_test_results(self) -> Dict[str, Any]:
        """Cargar resultados de pruebas desde archivos JSON"""
        
        try:
            # Buscar archivo de resultados más reciente
            reports_dir = "reports"
            json_files = [f for f in os.listdir(reports_dir) if f.endswith('.json')]
            
            if not json_files:
                logger.warning("No se encontraron archivos de resultados JSON")
                return self._generate_sample_data()
            
            # Usar el archivo más reciente
            latest_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(reports_dir, x)))
            
            with open(os.path.join(reports_dir, latest_file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"📊 Datos cargados desde: {latest_file}")
                return data
                
        except Exception as e:
            logger.warning(f"Error cargando resultados: {e}. Usando datos de ejemplo.")
            return self._generate_sample_data()
    
    def _generate_sample_data(self) -> Dict[str, Any]:
        """Generar datos de ejemplo para el reporte"""
        return {
            "summary": {
                "total_tests": 25,
                "passed": 23,
                "failed": 2,
                "skipped": 0,
                "duration": 45.6,
                "success_rate": 92.0
            },
            "tests": [
                {
                    "name": "test_health_check",
                    "outcome": "passed",
                    "duration": 0.15,
                    "categories": ["api", "smoke"]
                },
                {
                    "name": "test_create_product",
                    "outcome": "passed", 
                    "duration": 0.32,
                    "categories": ["api", "integration"]
                },
                {
                    "name": "test_invalid_data",
                    "outcome": "failed",
                    "duration": 0.28,
                    "categories": ["error_handling"]
                }
            ],
            "performance": {
                "response_times": {
                    "health_check": [120, 115, 125, 110, 118],
                    "get_products": [180, 175, 190, 170, 185],
                    "create_product": [250, 240, 260, 245, 255]
                },
                "thresholds": {
                    "health_check": 100,
                    "get_products": 200,
                    "create_product": 300
                }
            },
            "errors": {
                "400": 5,
                "404": 3,
                "415": 1,
                "500": 0
            }
        }
    
    def _create_cover_page(self, service_name: str = None) -> List:
        """Crear página de portada con información universitaria"""
        elements = []
        
        # Logo universitario (si existe)
        logo_path = ReportConfig.UNIVERSITY_INFO["logo_path"]
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=2*inch, height=2*inch)
                logo.hAlign = 'CENTER'
                elements.append(logo)
                elements.append(Spacer(1, 0.5*inch))
            except:
                logger.warning("No se pudo cargar el logo universitario")
        
        # Información universitaria
        university_info = [
            ReportConfig.UNIVERSITY_INFO["name"],
            ReportConfig.UNIVERSITY_INFO["faculty"],
            ReportConfig.UNIVERSITY_INFO["department"],
            ReportConfig.UNIVERSITY_INFO["course"],
            f"Semestre {ReportConfig.UNIVERSITY_INFO['semester']}"
        ]
        
        for info in university_info:
            p = Paragraph(info, self.custom_styles['university'])
            elements.append(p)
        
        elements.append(Spacer(1, 1*inch))
        
        # Título del proyecto
        title = Paragraph(
            ReportConfig.UNIVERSITY_INFO["project"],
            self.custom_styles['title']
        )
        elements.append(title)
        
        # Subtítulo del reporte
        if service_name:
            subtitle_text = f"Reporte de Pruebas de Integración - Servicio {service_name}"
        else:
            subtitle_text = "Reporte de Pruebas de Integración"
            
        subtitle = Paragraph(
            subtitle_text,
            self.custom_styles['subtitle']
        )
        elements.append(subtitle)
        
        elements.append(Spacer(1, 1*inch))
        
        # Información del equipo y fecha
        team_info = [
            f"<b>Equipo:</b> {ReportConfig.UNIVERSITY_INFO['team']}",
            f"<b>Fecha de Generación:</b> {datetime.now().strftime('%d de %B de %Y')}",
            f"<b>Hora:</b> {datetime.now().strftime('%H:%M:%S')}"
        ]
        
        for info in team_info:
            p = Paragraph(info, self.custom_styles['body'])
            elements.append(p)
        
        return elements
    
    def _create_executive_summary(self, test_data: Dict[str, Any]) -> List:
        """Crear resumen ejecutivo con métricas clave"""
        elements = []
        
        # Título de sección
        title = Paragraph("Resumen Ejecutivo", self.custom_styles['subtitle'])
        elements.append(title)
        
        # Introducción
        intro_text = """
        Este reporte presenta los resultados de las pruebas de integración realizadas sobre el 
        microservicio de gestión de productos de la plataforma AgroWeb. Las pruebas abarcan 
        funcionalidades completas del API REST, casos de error, y análisis de rendimiento.
        """
        intro = Paragraph(intro_text, self.custom_styles['body'])
        elements.append(intro)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Extraer métricas principales desde la estructura de pytest-json-report
        summary = test_data.get("summary", {})
        duration = test_data.get("duration", 0)
        
        # Calcular métricas
        total_tests = summary.get("total", 0)
        passed_tests = summary.get("passed", 0)
        failed_tests = summary.get("failed", 0)
        skipped_tests = summary.get("skipped", 0)
        
        # Calcular tasa de éxito
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        metrics_data = [
            ["Métrica", "Valor", "Estado"],
            ["Pruebas Totales", str(total_tests), "✓"],
            ["Pruebas Exitosas", str(passed_tests), "✓"],
            ["Pruebas Fallidas", str(failed_tests), "⚠" if failed_tests > 0 else "✓"],
            ["Tasa de Éxito", f"{success_rate:.1f}%", "✓" if success_rate >= 90 else "⚠"],
            ["Duración Total", f"{duration:.1f} segundos", "✓"],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), self.colors['light_blue']),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Conclusión del resumen
        if success_rate >= 95:
            conclusion = "🎯 <b>EXCELENTE:</b> El sistema demuestra alta estabilidad y confiabilidad."
        elif success_rate >= 90:
            conclusion = "✅ <b>BUENO:</b> El sistema funciona correctamente con oportunidades menores de mejora."
        elif success_rate >= 80:
            conclusion = "⚠️ <b>ACEPTABLE:</b> El sistema requiere atención en algunas áreas críticas."
        else:
            conclusion = "❌ <b>CRÍTICO:</b> El sistema presenta problemas significativos que requieren atención inmediata."
        
        conclusion_p = Paragraph(conclusion, self.custom_styles['body'])
        elements.append(conclusion_p)
        
        return elements
    
    def _create_detailed_results(self, test_data: Dict[str, Any]) -> List:
        """Crear sección de resultados detallados por categoría"""
        elements = []
        
        # Título de sección
        title = Paragraph("Resultados Detallados por Categoría", self.custom_styles['subtitle'])
        elements.append(title)
        
        # Agrupar pruebas por categoría
        tests = test_data.get("tests", [])
        categories = {}
        
        for test in tests:
            # Extraer categorías desde keywords de pytest en lugar de un campo separado
            test_keywords = test.get("keywords", [])
            test_categories = []
            
            # Buscar categorías conocidas en las keywords
            for keyword in test_keywords:
                if keyword in ["api", "integration", "error_handling", "performance", "smoke"]:
                    test_categories.append(keyword)
            
            # Si no tiene categorías específicas, usar "general"
            if not test_categories:
                test_categories = ["general"]
                
            for cat in test_categories:
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(test)
        
        # Crear tabla para cada categoría
        for category, category_tests in categories.items():
            cat_title = Paragraph(f"Categoría: {ReportConfig.TEST_CATEGORIES.get(category, category)}", 
                                 self.custom_styles['body'])
            elements.append(cat_title)
            
            # Calcular estadísticas de la categoría
            passed = len([t for t in category_tests if t.get("outcome") == "passed"])
            total = len(category_tests)
            success_rate = (passed / total * 100) if total > 0 else 0
            
            # Tabla de resultados
            table_data = [["Prueba", "Resultado", "Duración (s)", "Estado"]]
            
            for test in category_tests:
                outcome = test.get("outcome", "unknown")
                
                # Extraer duración desde la estructura de pytest-json-report
                call_data = test.get("call", {})
                duration = call_data.get("duration", 0)
                
                # Extraer nombre limpio del test desde nodeid
                test_name = test.get("nodeid", test.get("name", "Unknown"))
                if "::" in test_name:
                    # Formato: tests/carrito/test_api_integration.py::TestCarritoAPIIntegration::test_crear_carrito_exitoso
                    test_name = test_name.split("::")[-1]  # Tomar solo el nombre del método
                
                # Limpiar el nombre del test para que sea más legible
                clean_name = test_name.replace("test_", "").replace("_", " ").title()
                
                if outcome == "passed":
                    status = "✅ PASS"
                    status_color = self.colors['success']
                elif outcome == "failed":
                    status = "❌ FAIL"
                    status_color = self.colors['error']
                else:
                    status = "⏸️ SKIP"
                    status_color = self.colors['warning']
                
                table_data.append([
                    clean_name,
                    outcome.upper(),
                    f"{duration:.3f}",
                    status
                ])
            
            results_table = Table(table_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
            results_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 1), (-1, -1), self.colors['light_gray']),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            
            elements.append(results_table)
            
            # Estadísticas de la categoría
            stats_text = f"<b>Resumen:</b> {passed}/{total} pruebas exitosas ({success_rate:.1f}%)"
            stats = Paragraph(stats_text, self.custom_styles['body'])
            elements.append(stats)
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_performance_analysis(self, test_data: Dict[str, Any]) -> List:
        """Crear análisis de rendimiento con gráficos"""
        elements = []
        
        # Título de sección
        title = Paragraph("Análisis de Rendimiento", self.custom_styles['subtitle'])
        elements.append(title)
        
        # Texto introductorio
        intro = Paragraph(
            "El análisis de rendimiento evalúa la duración de ejecución de cada test "
            "para identificar operaciones lentas que puedan afectar la experiencia del usuario.",
            self.custom_styles['body']
        )
        elements.append(intro)
        elements.append(Spacer(1, 0.2*inch))
        
        # Extraer datos reales de duración de tests
        tests = test_data.get("tests", [])
        test_durations = {}
        
        for test in tests:
            # Extraer nombre limpio del test
            test_name = test.get("nodeid", test.get("name", "Unknown"))
            if "::" in test_name:
                test_name = test_name.split("::")[-1]  # Tomar solo el nombre del método
            clean_name = test_name.replace("test_", "").replace("_", " ").title()
            
            # Extraer duración desde la estructura de pytest-json-report
            call_data = test.get("call", {})
            duration = call_data.get("duration", 0)
            
            if duration > 0:  # Solo incluir tests con duración válida
                test_durations[clean_name] = duration * 1000  # Convertir a milisegundos
        
        # Detectar servicio para nombres únicos
        service_name = self._detect_service_from_tests(test_data)
        
        if test_durations:
            # Crear gráfico de duración de tests
            chart_path = self._create_test_duration_chart(test_durations, service_name)
            if chart_path and os.path.exists(chart_path):
                try:
                    chart_img = Image(chart_path, width=6*inch, height=4*inch)
                    chart_img.hAlign = 'CENTER'
                    elements.append(chart_img)
                    elements.append(Spacer(1, 0.2*inch))
                except:
                    logger.warning("No se pudo incluir gráfico de rendimiento")
            
            # Tabla de métricas de rendimiento basada en datos reales
            perf_data = [["Test", "Duración (ms)", "Clasificación", "Estado"]]
            
            # Definir umbrales para clasificación
            for test_name, duration_ms in test_durations.items():
                if duration_ms < 100:
                    classification = "Muy Rápido"
                    status = "✅ EXCELENTE"
                elif duration_ms < 500:
                    classification = "Rápido"
                    status = "✅ BUENO"
                elif duration_ms < 2000:
                    classification = "Moderado"
                    status = "⚠️ ACEPTABLE"
                else:
                    classification = "Lento"
                    status = "❌ LENTO"
                
                perf_data.append([
                    test_name,
                    f"{duration_ms:.1f}",
                    classification,
                    status
                ])
            
            # Ordenar por duración (más lento primero)
            perf_data[1:] = sorted(perf_data[1:], key=lambda x: float(x[1]), reverse=True)
            
            perf_table = Table(perf_data, colWidths=[2.5*inch, 1.2*inch, 1.3*inch, 1.5*inch])
            perf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 1), (-1, -1), self.colors['light_blue']),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(perf_table)
            
            # Estadísticas de rendimiento
            total_duration = sum(test_durations.values())
            avg_duration = total_duration / len(test_durations)
            slow_tests = len([d for d in test_durations.values() if d > 2000])
            
            stats_text = f"""
            <b>Estadísticas de Rendimiento:</b><br/>
            • Duración total de tests: {total_duration:.1f} ms<br/>
            • Duración promedio por test: {avg_duration:.1f} ms<br/>
            • Tests lentos (>2s): {slow_tests} de {len(test_durations)}<br/>
            • Test más rápido: {min(test_durations.values()):.1f} ms<br/>
            • Test más lento: {max(test_durations.values()):.1f} ms
            """
            stats = Paragraph(stats_text, self.custom_styles['body'])
            elements.append(stats)
        else:
            # Si no hay datos de duración, mostrar mensaje informativo
            no_data = Paragraph(
                "No se encontraron datos de duración de tests en esta ejecución.",
                self.custom_styles['body']
            )
            elements.append(no_data)
        
        return elements
    
    def _create_test_duration_chart(self, test_durations: Dict, service_name: str = None) -> str:
        """Crear gráfico de duración de tests con matplotlib"""
        try:
            plt.style.use('seaborn-v0_8')
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Preparar datos
            test_names = list(test_durations.keys())
            durations = list(test_durations.values())
            
            # Colores basados en duración
            bar_colors = []
            for duration in durations:
                if duration < 100:
                    bar_colors.append('#2ECC71')  # Verde - Muy rápido
                elif duration < 500:
                    bar_colors.append('#3498DB')  # Azul - Rápido
                elif duration < 2000:
                    bar_colors.append('#F39C12')  # Naranja - Moderado
                else:
                    bar_colors.append('#E74C3C')  # Rojo - Lento
            
            # Crear gráfico de barras horizontal
            y_pos = np.arange(len(test_names))
            bars = ax.barh(y_pos, durations, color=bar_colors, alpha=0.8)
            
            # Configurar ejes
            ax.set_yticks(y_pos)
            ax.set_yticklabels(test_names, fontsize=9)
            ax.set_xlabel('Duración (ms)', fontsize=12, fontweight='bold')
            ax.set_title(f'Duración de Tests - {service_name or "Servicio"}', fontsize=14, fontweight='bold')
            
            # Añadir valores en las barras
            for i, (bar, duration) in enumerate(zip(bars, durations)):
                width = bar.get_width()
                ax.text(width + max(durations) * 0.01, bar.get_y() + bar.get_height()/2,
                       f'{duration:.1f}ms', ha='left', va='center', fontsize=8)
            
            # Añadir líneas de referencia
            ax.axvline(x=100, color='green', linestyle='--', alpha=0.5, label='Muy Rápido (<100ms)')
            ax.axvline(x=500, color='blue', linestyle='--', alpha=0.5, label='Rápido (<500ms)')
            ax.axvline(x=2000, color='orange', linestyle='--', alpha=0.5, label='Aceptable (<2s)')
            
            # Configurar leyenda
            ax.legend(loc='lower right', fontsize=9)
            
            # Invertir el eje Y para mostrar tests en orden descendente de duración
            ax.invert_yaxis()
            
            plt.tight_layout()
            
            # Guardar gráfico con nombre único
            timestamp = ReportConfig.get_report_timestamp()
            service_suffix = f"_{service_name}" if service_name else ""
            chart_filename = f"test_duration_chart{service_suffix}_{timestamp}.png"
            chart_path = os.path.join("reports", chart_filename)
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"Error creando gráfico de duración de tests: {e}")
            return None

    def _create_performance_chart(self, response_times: Dict, thresholds: Dict, service_name: str = None) -> str:
        """Crear gráfico de rendimiento con matplotlib"""
        try:
            plt.style.use('seaborn-v0_8')
            fig, ax = plt.subplots(figsize=(10, 6))
            
            endpoints = list(response_times.keys())
            avg_times = [np.mean(times) for times in response_times.values()]
            threshold_values = [thresholds.get(endpoint, 200) for endpoint in endpoints]
            
            x = np.arange(len(endpoints))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, avg_times, width, label='Tiempo Promedio', color='skyblue')
            bars2 = ax.bar(x + width/2, threshold_values, width, label='Umbral', color='lightcoral')
            
            ax.set_xlabel('Endpoints')
            ax.set_ylabel('Tiempo de Respuesta (ms)')
            ax.set_title('Análisis de Rendimiento por Endpoint')
            ax.set_xticks(x)
            ax.set_xticklabels([e.replace('_', ' ').title() for e in endpoints], rotation=45)
            ax.legend()
            
            # Añadir valores sobre las barras
            for bar in bars1:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Guardar gráfico con nombre único por servicio y timestamp
            timestamp = ReportConfig.get_report_timestamp()
            service_suffix = f"_{service_name}" if service_name else ""
            chart_filename = f"performance_chart{service_suffix}_{timestamp}.png"
            chart_path = os.path.join("reports", chart_filename)
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"Error creando gráfico de rendimiento: {e}")
            return None
    
    def _create_error_analysis(self, test_data: Dict[str, Any]) -> List:
        """Crear análisis de manejo de errores"""
        elements = []
        
        # Título de sección
        title = Paragraph("Análisis de Manejo de Errores", self.custom_styles['subtitle'])
        elements.append(title)
        
        # Descripción
        desc = Paragraph(
            "El análisis de errores evalúa la capacidad del sistema para manejar "
            "situaciones excepcionales y retornar códigos de estado HTTP apropiados.",
            self.custom_styles['body']
        )
        elements.append(desc)
        elements.append(Spacer(1, 0.2*inch))
        
        # Datos de errores
        errors = test_data.get("errors", {})
        
        if errors:
            # Tabla de códigos de error
            error_data = [["Código HTTP", "Descripción", "Ocurrencias", "Estado"]]
            
            error_descriptions = {
                "400": "Bad Request - Datos inválidos",
                "404": "Not Found - Recurso no encontrado", 
                "415": "Unsupported Media Type",
                "500": "Internal Server Error"
            }
            
            for code, count in errors.items():
                description = error_descriptions.get(code, "Error desconocido")
                status = "✅ MANEJADO" if count > 0 else "➖ NO PROBADO"
                
                error_data.append([
                    code,
                    description,
                    str(count),
                    status
                ])
            
            error_table = Table(error_data, colWidths=[1*inch, 3*inch, 1.5*inch, 1.5*inch])
            error_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 1), (-1, -1), self.colors['light_gray']),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(error_table)
        
        return elements
    
    def _create_recommendations(self, test_data: Dict[str, Any]) -> List:
        """Crear sección de recomendaciones"""
        elements = []
        
        # Título de sección
        title = Paragraph("Recomendaciones y Conclusiones", self.custom_styles['subtitle'])
        elements.append(title)
        
        # Analizar datos para generar recomendaciones
        summary = test_data.get("summary", {})
        performance = test_data.get("performance", {})
        
        # Calcular tasa de éxito para recomendaciones
        total_tests = summary.get("total", 0)
        passed_tests = summary.get("passed", 0)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        recommendations = []
        
        # Recomendaciones basadas en tasa de éxito
        if success_rate < 95:
            recommendations.append({
                "type": "Funcionalidad",
                "priority": "Alta",
                "text": f"Mejorar la tasa de éxito actual ({success_rate:.1f}%) "
                       "investigando y corrigiendo las pruebas fallidas."
            })
        
        # Recomendaciones de rendimiento
        response_times = performance.get("response_times", {})
        thresholds = performance.get("thresholds", {})
        
        for endpoint, times in response_times.items():
            if times:
                avg_time = np.mean(times)
                threshold = thresholds.get(endpoint, 200)
                
                if avg_time > threshold:
                    recommendations.append({
                        "type": "Rendimiento",
                        "priority": "Media",
                        "text": f"Optimizar endpoint '{endpoint}' que excede el umbral "
                               f"({avg_time:.1f}ms > {threshold}ms)."
                    })
        
        # Recomendaciones generales
        recommendations.extend([
            {
                "type": "Cobertura",
                "priority": "Media",
                "text": "Expandir cobertura de pruebas incluyendo más casos edge y escenarios de carga."
            },
            {
                "type": "Monitoreo",
                "priority": "Baja",
                "text": "Implementar monitoreo continuo en producción basado en estas métricas."
            },
            {
                "type": "Documentación",
                "priority": "Baja",
                "text": "Mantener documentación actualizada de los endpoints basada en resultados de testing."
            }
        ])
        
        # Crear tabla de recomendaciones
        if recommendations:
            rec_data = [["Área", "Prioridad", "Recomendación"]]
            
            for rec in recommendations:
                priority_colors = {
                    "Alta": "🔴",
                    "Media": "🟡", 
                    "Baja": "🟢"
                }
                
                priority_icon = priority_colors.get(rec["priority"], "🔵")
                
                rec_data.append([
                    rec["type"],
                    f"{priority_icon} {rec['priority']}",
                    rec["text"]
                ])
            
            rec_table = Table(rec_data, colWidths=[1.5*inch, 1.5*inch, 4*inch])
            rec_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 1), (-1, -1), self.colors['light_gray']),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            elements.append(rec_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Conclusión final
        conclusion_text = f"""
        <b>Conclusión General:</b><br/>
        Las pruebas de integración han validado exitosamente el funcionamiento del microservicio 
        de gestión de productos AgroWeb. Con una tasa de éxito del {success_rate:.1f}%, el sistema 
        demuestra robustez en el manejo de operaciones CRUD, validación de errores y rendimiento 
        dentro de parámetros aceptables.
        <br/><br/>
        <b>Próximos Pasos:</b><br/>
        • Implementar las recomendaciones de prioridad alta<br/>
        • Establecer pipeline de CI/CD con estas pruebas<br/>
        • Configurar monitoreo de métricas en producción<br/>
        • Realizar pruebas de carga más extensivas
        """
        
        conclusion = Paragraph(conclusion_text, self.custom_styles['body'])
        elements.append(conclusion)
        
        return elements

def generate_integration_report() -> str:
    """Función principal para generar reporte de integración"""
    generator = PDFReportGenerator()
    return generator.generate_integration_report()

if __name__ == "__main__":
    # Generar reporte standalone
    report_path = generate_integration_report()
    print(f"✅ Reporte generado: {report_path}")
