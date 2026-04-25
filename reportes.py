"""
Módulo de generación de reportes.
Genera reportes independientes en archivos CSV y TXT en data/processed/
"""

import pandas as pd
from pathlib import Path
from datetime import datetime


def obtener_ruta_processed():
    """Obtiene la ruta de la carpeta processed."""
    ruta = Path(_file_).parent / "data" / "processed"
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def generar_timestamp():
    """Genera un timestamp para los archivos."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def guardar_reporte_txt(nombre_archivo, titulo, contenido):
    """Guarda un reporte en formato texto."""
    ruta = obtener_ruta_processed() / nombre_archivo
    
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write(f"  {titulo}\n")
        f.write("="*80 + "\n\n")
        f.write(contenido)
    
    print(f"  ✅ Reporte guardado: {nombre_archivo}")
    return ruta


def generar_reporte_desempeño(datos):
    """Genera reporte independiente de desempeño académico."""
    from analisis import (
        promedio_por_estudiante, promedio_por_tipo_evaluacion,
        promedio_por_materia, promedio_por_grupo, ranking_estudiantes,
        estudiantes_bajo_desempeño
    )
    
    print("\n📊 Generando reporte de DESEMPEÑO ACADÉMICO...")
    
    contenido = ""
    
    # 1. Promedio por estudiante (Top 10)
    promedio_est = promedio_por_estudiante(datos['calificaciones'], datos['matriculas'], datos['estudiantes'])
    contenido += "1. PROMEDIO POR ESTUDIANTE (Top 10)\n"
    contenido += "-" * 80 + "\n"
    contenido += promedio_est.head(10).to_string(index=False) + "\n\n"
    
    # 2. Promedio por tipo de evaluación
    promedio_tipo = promedio_por_tipo_evaluacion(datos['calificaciones'])
    contenido += "2. PROMEDIO POR TIPO DE EVALUACIÓN\n"
    contenido += "-" * 80 + "\n"
    contenido += promedio_tipo.to_string() + "\n\n"
    
    # 3. Promedio por materia
    promedio_mat = promedio_por_materia(datos['calificaciones'], datos['matriculas'], datos['grupos'], datos['materias'])
    contenido += "3. PROMEDIO POR MATERIA\n"
    contenido += "-" * 80 + "\n"
    contenido += promedio_mat.to_string() + "\n\n"