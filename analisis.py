"""
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


def promedio_por_tipo_evaluacion(df_calificaciones):
    """Calcula promedio por tipo de evaluación (PARCIAL_1, PARCIAL_2, EXAMEN_FINAL, TRABAJO)."""
    promedio_tipo = df_calificaciones.groupby('tipo')[['nota']].agg(['mean', 'count', 'std']).round(2)
    promedio_tipo.columns = ['promedio', 'cantidad', 'desviacion_std']
    return promedio_tipo


def promedio_por_materia(df_calificaciones, df_matriculas, df_grupos, df_materias):
    """Calcula promedio de calificaciones por materia."""
    # Merge para obtener materia_id
    cal_with_mat = df_calificaciones.merge(df_matriculas[['id', 'grupo_id']], left_on='matricula_id', right_on='id')
    cal_with_mat = cal_with_mat.merge(df_grupos[['id', 'materia_id']], left_on='grupo_id', right_on='id', suffixes=('_cal', '_grup'))
    cal_with_mat = cal_with_mat.merge(df_materias[['id', 'nombre']], left_on='materia_id', right_on='id', suffixes=('_mat', '_mat_materias'))
    
    promedio = cal_with_mat.groupby('nombre')[['nota']].agg(['mean', 'count']).round(2)
    promedio.columns = ['promedio', 'cantidad_calificaciones']
    return promedio.sort_values('promedio', ascending=False)


def promedio_por_grupo(df_calificaciones, df_matriculas, df_grupos, df_materias):
    """Calcula promedio de calificaciones por grupo."""
    cal_with_grup = df_calificaciones.merge(df_matriculas[['id', 'grupo_id']], left_on='matricula_id', right_on='id')
    cal_with_grup = cal_with_grup.merge(df_grupos[['id', 'nombre', 'semestre', 'materia_id']], left_on='grupo_id', right_on='id', suffixes=('_mat', '_grup'))
    
    promedio = cal_with_grup.groupby(['nombre', 'semestre'])[['nota']].agg(['mean', 'count']).round(2)
    promedio.columns = ['promedio', 'cantidad_calificaciones']
    return promedio.sort_values('promedio', ascending=False)


def ranking_estudiantes(df_calificaciones, df_matriculas, df_estudiantes):
    """Genera ranking de mejores y peores estudiantes."""
    promedio = promedio_por_estudiante(df_calificaciones, df_matriculas, df_estudiantes)
    
    ranking = {
        'mejores': promedio.head(5),
        'peores': promedio.tail(5)
    }
    return ranking


def estudiantes_bajo_desempeño(df_calificaciones, df_matriculas, df_estudiantes, umbral=3.0):
    """Identifica estudiantes con desempeño bajo (promedio < umbral)."""
    promedio = promedio_por_estudiante(df_calificaciones, df_matriculas, df_estudiantes)
    bajo_desempeño = promedio[promedio['promedio'] < umbral]
    return bajo_desempeño.sort_values('promedio')