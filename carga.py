"""
Módulo de carga de datos.
Responsable de leer los archivos CSV desde data/raw/ y convertirlos en DataFrames.
"""

import pandas as pd
from pathlib import Path


def obtener_ruta_base():
    """Obtiene la ruta base del proyecto."""
    return Path(__file__).parent


def cargar_estudiantes():
    """Carga el archivo de estudiantes."""
    ruta = obtener_ruta_base() / "data" / "raw" / "estudiantes.txt"
    return pd.read_csv(ruta)


def cargar_profesores():
    """Carga el archivo de profesores."""
    ruta = obtener_ruta_base() / "data" / "raw" / "profesores.txt"
    return pd.read_csv(ruta)


def cargar_programas_academicos():
    """Carga el archivo de programas académicos."""
    ruta = obtener_ruta_base() / "data" / "raw" / "programas_academicos.txt"
    return pd.read_csv(ruta)


def cargar_materias():
    """Carga el archivo de materias."""
    ruta = obtener_ruta_base() / "data" / "raw" / "materias.txt"
    return pd.read_csv(ruta)


def cargar_grupos():
    """Carga el archivo de grupos."""
    ruta = obtener_ruta_base() / "data" / "raw" / "grupos.txt"
    return pd.read_csv(ruta)


def cargar_matriculas():
    """Carga el archivo de matrículas."""
    ruta = obtener_ruta_base() / "data" / "raw" / "matriculas.txt"
    return pd.read_csv(ruta)


def cargar_calificaciones():
    """Carga el archivo de calificaciones."""
    ruta = obtener_ruta_base() / "data" / "raw" / "calificaciones.txt"
    return pd.read_csv(ruta)


def cargar_todos_datos():
    """
    Carga todos los datos y retorna un diccionario con DataFrames.
    Útil para orquestar la carga completa en main.py
    """
    datos = {
        'estudiantes': cargar_estudiantes(),
        'profesores': cargar_profesores(),
        'programas_academicos': cargar_programas_academicos(),
        'materias': cargar_materias(),
        'grupos': cargar_grupos(),
        'matriculas': cargar_matriculas(),
        'calificaciones': cargar_calificaciones()
    }
    return datos
