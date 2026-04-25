Módulo de análisis de datos.
Implementa todos los análisis solicitados: desempeño, distribución, profesores y calidad.
"""

import pandas as pd
import numpy as np


# ============================================================================
# 1. ANÁLISIS DE DESEMPEÑO ACADÉMICO
# ============================================================================

def promedio_por_estudiante(df_calificaciones, df_matriculas, df_estudiantes):
    """Calcula el promedio general de cada estudiante."""
    # Merge para obtener estudiante_id
    cal_with_est = df_calificaciones.merge(df_matriculas[['id', 'estudiante_id']], left_on='matricula_id', right_on='id')
    cal_with_est = cal_with_est.merge(df_estudiantes[['id', 'nombres', 'apellidos']], left_on='estudiante_id', right_on='id', suffixes=('_mat', '_est'))
    
    # Agrupar por estudiante y calcular promedio
    promedio = cal_with_est.groupby('estudiante_id')[['nota']].mean().rename(columns={'nota': 'promedio'})
    promedio = promedio.merge(df_estudiantes[['id', 'nombres', 'apellidos']], left_index=True, right_on='id')
    promedio = promedio.sort_values('promedio', ascending=False)
    
    return promedio[['nombres', 'apellidos', 'promedio']]
