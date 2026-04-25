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
    
    # 4. Promedio por grupo
    promedio_grup = promedio_por_grupo(datos['calificaciones'], datos['matriculas'], datos['grupos'], datos['materias'])
    contenido += "4. PROMEDIO POR GRUPO\n"
    contenido += "-" * 80 + "\n"
    contenido += promedio_grup.head(15).to_string() + "\n\n"
    
    # 5. Ranking
    ranking = ranking_estudiantes(datos['calificaciones'], datos['matriculas'], datos['estudiantes'])
    contenido += "5. RANKING - MEJORES ESTUDIANTES\n"
    contenido += "-" * 80 + "\n"
    contenido += ranking['mejores'].to_string(index=False) + "\n\n"
    
    contenido += "6. RANKING - PEORES ESTUDIANTES\n"
    contenido += "-" * 80 + "\n"
    contenido += ranking['peores'].to_string(index=False) + "\n\n"
    
    # 6. Bajo desempeño
    bajo_desempeño = estudiantes_bajo_desempeño(datos['calificaciones'], datos['matriculas'], datos['estudiantes'], umbral=3.0)
    contenido += "7. ESTUDIANTES CON BAJO DESEMPEÑO (promedio < 3.0)\n"
    contenido += "-" * 80 + "\n"
    if len(bajo_desempeño) > 0:
        contenido += bajo_desempeño.to_string(index=False)
    else:
        contenido += "✅ No hay estudiantes con bajo desempeño"
    contenido += "\n\n"
    
    guardar_reporte_txt("01_DESEMPEÑO_ACADEMICO.txt", "REPORTE DE DESEMPEÑO ACADÉMICO", contenido)
    
    # Guardar datos detallados en CSV
    promedio_est.to_csv(obtener_ruta_processed() / "01_promedio_por_estudiante.csv", index=False)
    promedio_mat.to_csv(obtener_ruta_processed() / "01_promedio_por_materia.csv")
    print("  ✅ Archivos CSV generados")


def generar_reporte_distribucion(datos):
    """Genera reporte independiente de distribución."""
    from analisis import (
        estudiantes_por_programa, estudiantes_por_semestre,
        ocupacion_grupos, materias_mas_demandadas, estudiantes_por_modalidad
    )
    
    print("\n📈 Generando reporte de DISTRIBUCIÓN...")
    
    contenido = ""
    
    # 1. Estudiantes por programa
    est_prog = estudiantes_por_programa(datos['estudiantes'], datos['programas_academicos'])
    contenido += "1. ESTUDIANTES POR PROGRAMA ACADÉMICO\n"
    contenido += "-" * 80 + "\n"
    contenido += est_prog.to_string(index=False) + "\n\n"
    
    # 2. Estudiantes por semestre
    est_sem = estudiantes_por_semestre(datos['matriculas'], datos['grupos'])
    contenido += "2. ESTUDIANTES POR SEMESTRE\n"
    contenido += "-" * 80 + "\n"
    contenido += est_sem.to_string(index=False) + "\n\n"
    
    # 3. Ocupación de grupos
    ocupacion = ocupacion_grupos(datos['matriculas'], datos['grupos'])
    contenido += "3. OCUPACIÓN DE GRUPOS\n"
    contenido += "-" * 80 + "\n"
    contenido += ocupacion.to_string(index=False) + "\n\n"
    
    # 4. Materias más demandadas
    materias = materias_mas_demandadas(datos['matriculas'], datos['grupos'], datos['materias'])
    contenido += "4. MATERIAS MÁS DEMANDADAS\n"
    contenido += "-" * 80 + "\n"
    contenido += materias.to_string(index=False) + "\n\n"
    
    # 5. Estudiantes por modalidad
    modalidad = estudiantes_por_modalidad(datos['estudiantes'], datos['programas_academicos'])
    contenido += "5. ESTUDIANTES POR MODALIDAD\n"
    contenido += "-" * 80 + "\n"
    contenido += modalidad.to_string(index=False) + "\n\n"
    
    guardar_reporte_txt("02_DISTRIBUCIÓN.txt", "REPORTE DE DISTRIBUCIÓN", contenido)
    
    # Guardar datos detallados en CSV
    est_prog.to_csv(obtener_ruta_processed() / "02_estudiantes_por_programa.csv", index=False)
    ocupacion.to_csv(obtener_ruta_processed() / "02_ocupacion_grupos.csv", index=False)
    print("  ✅ Archivos CSV generados")


def generar_reporte_profesores(datos):
    """Genera reporte independiente de análisis de profesores."""
    from analisis import (
        carga_academica_profesores, estudiantes_por_profesor,
        desempeño_estudiantes_por_profesor, profesores_datos_incompletos
    )
    
    print("\n👥 Generando reporte de PROFESORES...")
    
    contenido = ""
    
    # 1. Carga académica
    carga = carga_academica_profesores(datos['grupos'], datos['profesores'])
    contenido += "1. CARGA ACADÉMICA (GRUPOS POR PROFESOR)\n"
    contenido += "-" * 80 + "\n"
    contenido += carga.to_string(index=False) + "\n\n"
    
    # 2. Estudiantes por profesor
    est_prof = estudiantes_por_profesor(datos['matriculas'], datos['grupos'], datos['profesores'])
    contenido += "2. CANTIDAD DE ESTUDIANTES POR PROFESOR\n"
    contenido += "-" * 80 + "\n"
    contenido += est_prof.to_string(index=False) + "\n\n"
    
    # 3. Desempeño según profesor
    desempeño_prof = desempeño_estudiantes_por_profesor(datos['calificaciones'], datos['matriculas'], datos['grupos'], datos['profesores'])
    contenido += "3. DESEMPEÑO PROMEDIO DE ESTUDIANTES POR PROFESOR\n"
    contenido += "-" * 80 + "\n"
    contenido += desempeño_prof.to_string(index=False) + "\n\n"
    
    # 4. Profesores con datos incompletos
    prof_incompletos = profesores_datos_incompletos(datos['profesores'])
    contenido += "4. PROFESORES CON DATOS INCOMPLETOS\n"
    contenido += "-" * 80 + "\n"
    if len(prof_incompletos) > 0:
        contenido += prof_incompletos.to_string(index=False)
    else:
        contenido += "✅ Todos los profesores tienen datos completos"
    contenido += "\n\n"
    
    guardar_reporte_txt("03_PROFESORES.txt", "REPORTE DE ANÁLISIS DE PROFESORES", contenido)
    
    # Guardar datos detallados en CSV
    carga.to_csv(obtener_ruta_processed() / "03_carga_academica.csv", index=False)
    est_prof.to_csv(obtener_ruta_processed() / "03_estudiantes_por_profesor.csv", index=False)
    desempeño_prof.to_csv(obtener_ruta_processed() / "03_desempeño_por_profesor.csv", index=False)
    print("  ✅ Archivos CSV generados")


def generar_reporte_calidad(datos):
    """Genera reporte independiente de calidad de datos."""
    from limpieza import (
        reporte_calidad_estudiantes, reporte_calidad_profesores,
        reporte_calidad_grupos, reporte_calidad_matriculas,
        reporte_calidad_calificaciones, validar_email, validar_celular
    )
    import io
    from contextlib import redirect_stdout
    
    print("\n🔍 Generando reporte de CALIDAD DE DATOS...")
    
    contenido = ""
    
    # Capturar los reportes de limpieza
    f = io.StringIO()
    with redirect_stdout(f):
        reporte_calidad_estudiantes(datos['estudiantes'])
        reporte_calidad_profesores(datos['profesores'])
        reporte_calidad_grupos(datos['grupos'], datos['materias'], datos['profesores'])
        reporte_calidad_matriculas(datos['matriculas'], datos['grupos'], datos['estudiantes'])
        reporte_calidad_calificaciones(datos['calificaciones'], datos['matriculas'])
    
    contenido = f.getvalue()
    
    guardar_reporte_txt("04_CALIDAD_DATOS.txt", "REPORTE DE CALIDAD DE DATOS", contenido)
    print("  ✅ Reporte de calidad generado")


def generar_resumen_ejecutivo(datos):
    """Genera un resumen ejecutivo con las métricas principales."""
    from analisis import resumen_estadistico
    
    print("\n📋 Generando RESUMEN EJECUTIVO...")
    
    contenido = ""
    
    resumen = resumen_estadistico(datos)
    contenido += "MÉTRICAS GENERALES DEL SISTEMA\n"
    contenido += "-" * 80 + "\n"
    for key, value in resumen.items():
        contenido += f"  {key.replace('_', ' ').title()}: {value}\n"
    
    contenido += "\n" + "-" * 80 + "\n"
    contenido += "\nARCHIVOS GENERADOS:\n"
    contenido += "  - 01_DESEMPEÑO_ACADÉMICO.txt\n"
    contenido += "  - 02_DISTRIBUCIÓN.txt\n"
    contenido += "  - 03_PROFESORES.txt\n"
    contenido += "  - 04_CALIDAD_DATOS.txt\n"
    contenido += "  - RESUMEN_EJECUTIVO.txt\n"
    contenido += "\nArchivos CSV complementarios en data/processed/\n"
    
    guardar_reporte_txt("00_RESUMEN_EJECUTIVO.txt", "RESUMEN EJECUTIVO", contenido)
    print("  ✅ Resumen ejecutivo generado")


def generar_todos_reportes(datos):
    """Genera todos los reportes de manera independiente."""
    print("\n" + "█"*80)
    print("█ GENERANDO REPORTES INDEPENDIENTES EN data/processed/".ljust(79) + "█")
    print("█"*80)
    
    generar_reporte_desempeño(datos)
    generar_reporte_distribucion(datos)
    generar_reporte_profesores(datos)
    generar_reporte_calidad(datos)
    generar_resumen_ejecutivo(datos)
    
    print("\n" + "█"*80)
    print("█ TODOS LOS REPORTES HAN SIDO GENERADOS EXITOSAMENTE".ljust(79) + "█")
    print("█"*80)
    print(f"\n📁 Ubicación: {obtener_ruta_processed()}\n")