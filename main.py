"""
Módulo principal de orquestación.
Ejecuta la carga, limpieza y análisis de datos, generando reportes independientes en archivos.
"""

import sys
import pandas as pd
from carga import cargar_todos_datos, cargar_todos_datos_db
from limpieza import generar_reporte_completo_calidad
from reportes import generar_todos_reportes
from analisis import resumen_estadistico


def main():
    """Función principal que orquesta todo el análisis."""
    
    usar_db = "--db" in sys.argv or "-d" in sys.argv
    
    print("\n" + "█"*70)
    print("█ SISTEMA DE ANÁLISIS DE DATOS - SISTEMA DE NOTAS".ljust(69) + "█")
    print("█"*70)
    
    # ========================================================================
    # 1. CARGAR DATOS
    # ========================================================================
    print("\n" + "="*70)
    if usar_db:
        print("  1. CARGANDO DATOS DESDE PostgreSQL")
    else:
        print("  1. CARGANDO DATOS DESDE ARCHIVOS")
    print("="*70 + "\n")
    
    try:
        if usar_db:
            datos = cargar_todos_datos_db()
            print("✅ Datos cargados desde PostgreSQL correctamente.\n")
        else:
            datos = cargar_todos_datos()
            print("✅ Todos los datos han sido cargados correctamente.\n")
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        if usar_db:
            print("  Fallback: cargando desde archivos...")
            datos = cargar_todos_datos()
        else:
            sys.exit(1)
    
    # Resumen inicial
    resumen = resumen_estadistico(datos)
    for key, value in resumen.items():
        print(f"  📊 {key.replace('_', ' ').title()}: {value}")
    
    # ========================================================================
    # 2. REPORTE DE CALIDAD (CONSOLA)
    # ========================================================================
    generar_reporte_completo_calidad(datos)
    
    # ========================================================================
    # 3. GENERAR TODOS LOS REPORTES EN ARCHIVOS
    # ========================================================================
    generar_todos_reportes(datos)
    
    # ========================================================================
    # CIERRE
    # ========================================================================
    print("="*70)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
