import pandas as pd
from pathlib import Path

def obtener_ruta_base():
    return Path(__file__).parent

def cargar_estudiantes():
    ruta = obtener_ruta_base() / "data" / "raw" / "estudiantes.txt"
    return pd.read_csv(ruta)

def cargar_profesores():
    ruta = obtener_ruta_base() / "data" / "raw" / "profesores.txt"
    return pd.read_csv(ruta)

def cargar_programas_academicos():
    ruta = obtener_ruta_base() / "data" / "raw" / "programas_academicos.txt"
    return pd.read_csv(ruta)

def cargar_materias():
    ruta = obtener_ruta_base() / "data" / "raw" / "materias.txt"
    return pd.read_csv(ruta)
