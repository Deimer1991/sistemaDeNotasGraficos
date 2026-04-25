"""
Módulo principal de orquestación.
Ejecuta la carga, limpieza y análisis de datos, generando reportes independientes en archivos.
"""

import pandas as pd
from carga import cargar_todos_datos
from limpieza import generar_reporte_completo_calidad
from reportes import generar_todos_reportes
from analisis import resumen_estadistico


def main():
    """Función principal que orquesta todo el análisis."""
    
    print("\n" + "█"*70)
    print("█ SISTEMA DE ANÁLISIS DE DATOS - SISTEMA DE NOTAS".ljust(69) + "█")
    print("█"*70)
    
    # ========================================================================
    # 1. CARGAR DATOS
    # ========================================================================
    print("\n" + "="*70)
    print("  1. CARGANDO DATOS")
    print("="*70 + "\n")
    datos = cargar_todos_datos()
    print("✅ Todos los datos han sido cargados correctamente.\n")
    
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
