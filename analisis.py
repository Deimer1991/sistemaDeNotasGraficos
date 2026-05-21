"""
Módulo de análisis de datos.
Implementa todos los análisis solicitados: desempeño, distribución, profesores y calidad.
"""

import pandas as pd
import numpy as np


# ============================================================================
# 1. ANÁLISIS DE DESEMPEÑO ACADÉMICO
# ============================================================================

def promedio_por_estudiante(df_calificaciones, df_matriculas, df_estudiantes, df_programas=None):
    """Calcula el promedio general de cada estudiante."""
    # Merge para obtener estudiante_id
    cal_with_est = df_calificaciones.merge(df_matriculas[['id', 'estudiante_id']], left_on='matricula_id', right_on='id')
    cal_with_est = cal_with_est.merge(df_estudiantes[['id', 'nombres', 'apellidos', 'programa_id']], left_on='estudiante_id', right_on='id', suffixes=('_mat', '_est'))
    
    # Agrupar por estudiante y calcular promedio
    promedio = cal_with_est.groupby('estudiante_id')[['nota']].mean().rename(columns={'nota': 'promedio'})
    promedio = promedio.merge(df_estudiantes[['id', 'nombres', 'apellidos', 'programa_id']], left_index=True, right_on='id')
    promedio = promedio.sort_values('promedio', ascending=False)
    
    cols = ['nombres', 'apellidos', 'promedio']
    if df_programas is not None:
        promedio = promedio.merge(df_programas[['id', 'nombre']], left_on='programa_id', right_on='id', how='left')
        promedio = promedio.rename(columns={'nombre': 'programa'})
        cols.append('programa')
    
    return promedio[cols]


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


def ranking_estudiantes(df_calificaciones, df_matriculas, df_estudiantes, df_programas=None, top=10):
    """Genera ranking de mejores y peores estudiantes."""
    promedio = promedio_por_estudiante(df_calificaciones, df_matriculas, df_estudiantes, df_programas)
    
    ranking = {
        'mejores': promedio.head(top),
        'peores': promedio.tail(top).sort_values('promedio', ascending=True)
    }
    return ranking


def estudiantes_bajo_desempeño(df_calificaciones, df_matriculas, df_estudiantes, umbral=3.0, df_programas=None):
    """Identifica estudiantes con desempeño bajo (promedio < umbral)."""
    promedio = promedio_por_estudiante(df_calificaciones, df_matriculas, df_estudiantes, df_programas)
    bajo_desempeño = promedio[promedio['promedio'] < umbral]
    return bajo_desempeño.sort_values('promedio')

# ============================================================================
# 2. ANÁLISIS DE DISTRIBUCIÓN
# ============================================================================

def estudiantes_por_programa(df_estudiantes, df_programas):
    """Cuenta estudiantes por programa académico."""
    estudiantes_prog = df_estudiantes.groupby('programa_id').size().reset_index(name='cantidad_estudiantes')
    estudiantes_prog = estudiantes_prog.merge(df_programas[['id', 'nombre']], left_on='programa_id', right_on='id')
    return estudiantes_prog[['nombre', 'cantidad_estudiantes']].sort_values('cantidad_estudiantes', ascending=False)


def estudiantes_por_semestre(df_matriculas, df_grupos):
    """Cuenta estudiantes por semestre (2023-I vs 2023-II)."""
    matriculas_con_sem = df_matriculas.merge(df_grupos[['id', 'semestre']], left_on='grupo_id', right_on='id')
    estudiantes_sem = matriculas_con_sem.groupby('semestre').size().reset_index(name='cantidad_estudiantes')
    return estudiantes_sem.sort_values('cantidad_estudiantes', ascending=False)


def ocupacion_grupos(df_matriculas, df_grupos):
    """Calcula ocupación de cada grupo (estudiantes reales vs cupo máximo)."""
    matriculas_por_grupo = df_matriculas.groupby('grupo_id').size().reset_index(name='estudiantes_reales')
    ocupacion = matriculas_por_grupo.merge(df_grupos[['id', 'nombre', 'semestre', 'cupo_maximo']], left_on='grupo_id', right_on='id')
    ocupacion['porcentaje_ocupacion'] = (ocupacion['estudiantes_reales'] / ocupacion['cupo_maximo'] * 100).round(1)
    return ocupacion[['nombre', 'semestre', 'estudiantes_reales', 'cupo_maximo', 'porcentaje_ocupacion']].sort_values('porcentaje_ocupacion', ascending=False)


def materias_mas_demandadas(df_matriculas, df_grupos, df_materias):
    """Identifica las materias con más estudiantes inscritos."""
    mat_con_grup = df_matriculas.merge(df_grupos[['id', 'materia_id']], left_on='grupo_id', right_on='id')
    mat_con_mat = mat_con_grup.merge(df_materias[['id', 'nombre']], left_on='materia_id', right_on='id', suffixes=('_grup', '_mat'))
    
    demanda = mat_con_mat.groupby('nombre').size().reset_index(name='cantidad_estudiantes')
    return demanda.sort_values('cantidad_estudiantes', ascending=False)


def estudiantes_por_modalidad(df_estudiantes, df_programas):
    """Distribuye estudiantes por modalidad (Presencial vs Virtual)."""
    est_con_prog = df_estudiantes.merge(df_programas[['id', 'modalidad']], left_on='programa_id', right_on='id')
    modalidad = est_con_prog.groupby('modalidad').size().reset_index(name='cantidad_estudiantes')
    return modalidad


# ============================================================================
# 3. ANÁLISIS DE PROFESORES
# ============================================================================

def carga_academica_profesores(df_grupos, df_profesores):
    """Calcula cantidad de grupos por profesor."""
    carga = df_grupos.groupby('profesor_id').size().reset_index(name='cantidad_grupos')
    carga = carga.merge(df_profesores[['id', 'nombres', 'apellidos']], left_on='profesor_id', right_on='id')
    return carga[['nombres', 'apellidos', 'cantidad_grupos']].sort_values('cantidad_grupos', ascending=False)


def estudiantes_por_profesor(df_matriculas, df_grupos, df_profesores):
    """Calcula cantidad de estudiantes a cargo de cada profesor."""
    mat_con_grup = df_matriculas.merge(df_grupos[['id', 'profesor_id']], left_on='grupo_id', right_on='id')
    estudiantes = mat_con_grup.groupby('profesor_id').size().reset_index(name='cantidad_estudiantes')
    estudiantes = estudiantes.merge(df_profesores[['id', 'nombres', 'apellidos']], left_on='profesor_id', right_on='id')
    return estudiantes[['nombres', 'apellidos', 'cantidad_estudiantes']].sort_values('cantidad_estudiantes', ascending=False)


def desempeño_estudiantes_por_profesor(df_calificaciones, df_matriculas, df_grupos, df_profesores):
    """Calcula desempeño promedio de estudiantes según su profesor."""
    cal_with_est = df_calificaciones.merge(df_matriculas[['id', 'grupo_id']], left_on='matricula_id', right_on='id')
    cal_with_est = cal_with_est.merge(df_grupos[['id', 'profesor_id']], left_on='grupo_id', right_on='id', suffixes=('_mat', '_grup'))
    
    desempeño = cal_with_est.groupby('profesor_id')[['nota']].agg(['mean', 'count']).round(2)
    desempeño.columns = ['promedio_estudiantes', 'cantidad_calificaciones']
    desempeño = desempeño.reset_index()
    desempeño = desempeño.merge(df_profesores[['id', 'nombres', 'apellidos']], left_on='profesor_id', right_on='id')
    
    return desempeño[['nombres', 'apellidos', 'promedio_estudiantes', 'cantidad_calificaciones']].sort_values('promedio_estudiantes', ascending=False)


def profesores_datos_incompletos(df_profesores):
    """Identifica profesores con datos incompletos (sin email o celular válido)."""
    from limpieza import validar_email, validar_celular
    
    incompletos = []
    for idx, row in df_profesores.iterrows():
        problemas = []
        if not validar_email(row['correo']):
            problemas.append('sin_email_válido')
        if not validar_celular(row['numero_celular']):
            problemas.append('sin_celular_válido')
        
        if problemas:
            incompletos.append({
                'nombres': row['nombres'],
                'apellidos': row['apellidos'],
                'problemas': ', '.join(problemas)
            })
    
    return pd.DataFrame(incompletos) if incompletos else pd.DataFrame()


# ============================================================================
# 4. RESUMEN GENERAL
# ============================================================================

def resumen_estadistico(datos):
    def _activos(key):
        df = datos.get(key, pd.DataFrame())
        if df.empty or "estado" not in df.columns:
            return 0
        return len(df[df["estado"] == "ACTIVO"])

    resumen = {
        'total_estudiantes': _activos('estudiantes'),
        'total_profesores': _activos('profesores'),
        'total_administrativos': _activos('administrativos'),
        'total_programas': _activos('programas_academicos'),
        'total_materias': _activos('materias'),
        'total_grupos': _activos('grupos'),
    }
    
    return pd.Series(resumen)


def promedio_por_programa(df_calificaciones, df_matriculas, df_estudiantes, df_programas):
    """Calcula el promedio de notas por programa académico."""
    cal_with_est = df_calificaciones.merge(df_matriculas[['id', 'estudiante_id']], left_on='matricula_id', right_on='id')
    cal_with_est = cal_with_est.merge(df_estudiantes[['id', 'programa_id']], left_on='estudiante_id', right_on='id', suffixes=('_cal', '_est'))
    cal_with_est = cal_with_est.merge(df_programas[['id', 'nombre']], left_on='programa_id', right_on='id', suffixes=('_est', '_prog'))

    promedio = cal_with_est.groupby('nombre')[['nota']].agg(['mean', 'count']).round(2)
    promedio.columns = ['promedio', 'cantidad_calificaciones']
    return promedio.sort_values('promedio', ascending=False).reset_index()


def matriculados_por_ano(df_matriculas):
    """Cuenta matrículas agrupadas por año."""
    df = df_matriculas.copy()
    df['ano'] = pd.to_datetime(df['fecha_matricula']).dt.year
    matriculados = df.groupby('ano').size().reset_index(name='cantidad_matriculados')
    return matriculados.sort_values('ano')


def filtrar_por_programa(programa_id, datos):
    """Filtra los DataFrames de estudiantes, matrículas y calificaciones por programa."""
    if programa_id is None:
        return datos
    est_ids = datos['estudiantes'][datos['estudiantes']['programa_id'] == programa_id]['id']
    mat_ids = datos['matriculas'][datos['matriculas']['estudiante_id'].isin(est_ids)]['id']
    d = datos.copy()
    d['estudiantes'] = datos['estudiantes'][datos['estudiantes']['id'].isin(est_ids)]
    d['matriculas'] = datos['matriculas'][datos['matriculas']['id'].isin(mat_ids)]
    d['calificaciones'] = datos['calificaciones'][datos['calificaciones']['matricula_id'].isin(mat_ids)]
    return d


