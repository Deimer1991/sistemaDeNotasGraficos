import pandas as pd
from pathlib import Path
from database import obtener_engine

def obtener_ruta_base():
    return Path(__file__).parent

# ============================================================================
# CARGA DESDE ARCHIVOS (mock)
# ============================================================================

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
def cargar_grupos():
    ruta = obtener_ruta_base() / "data" / "raw" / "grupos.txt"
    return pd.read_csv(ruta)

def cargar_matriculas():
    ruta = obtener_ruta_base() / "data" / "raw" / "matriculas.txt"
    return pd.read_csv(ruta)

def cargar_calificaciones():
    ruta = obtener_ruta_base() / "data" / "raw" / "calificaciones.txt"
    return pd.read_csv(ruta)

def cargar_todos_datos():
    datos = {
        'estudiantes': cargar_estudiantes(),
        'profesores': cargar_profesores(),
        'administrativos': pd.DataFrame(),
        'programas_academicos': cargar_programas_academicos(),
        'materias': cargar_materias(),
        'grupos': cargar_grupos(),
        'matriculas': cargar_matriculas(),
        'calificaciones': cargar_calificaciones()
    }
    return datos 

def cargar_est_pro():
    ruta = obtener_ruta_base() / "data" / "processed" / "02_estudiantes_por_programa.csv"
    return pd.read_csv(ruta)

# ============================================================================
# CARGA DESDE BASE DE DATOS (PostgreSQL)
# ============================================================================

def _query_df(query, engine):
    return pd.read_sql_query(query, engine)


def cargar_estudiantes_db(engine=None):
    if engine is None:
        engine = obtener_engine()
    query = """
        SELECT u.id,
               u.fecha_registro AS fecha_creacion,
               u.fecha_actualizacion AS fecha_modificacion,
               u.nombres, u.apellidos,
               u.tipo_documento, u.documento,
               u.correo, u.numero_celular,
               u.rol, u.estado,
               u.envio_correo, u.token_registro, u.registro,
               u.token_recuperacion, u.expiracion_token_recuperacion,
               e.programa_id, e.foto
        FROM usuarios u
        JOIN estudiantes e ON u.id = e.id_usuario
        WHERE u.rol = 'ESTUDIANTE'
    """
    return _query_df(query, engine)


def cargar_profesores_db(engine=None):
    if engine is None:
        engine = obtener_engine()
    query = """
        SELECT u.id,
               u.fecha_registro AS fecha_creacion,
               u.fecha_actualizacion AS fecha_modificacion,
               u.nombres, u.apellidos,
               u.tipo_documento, u.documento,
               u.correo, u.numero_celular,
               u.rol, u.estado,
               u.envio_correo, u.token_registro, u.registro,
               u.token_recuperacion, u.expiracion_token_recuperacion,
               p.titulo AS titulo_profesional,
               p.especializacion, p.foto
        FROM usuarios u
        JOIN profesores p ON u.id = p.id_usuario
        WHERE u.rol = 'PROFESOR'
    """
    return _query_df(query, engine)


def cargar_programas_academicos_db(engine=None):
    if engine is None:
        engine = obtener_engine()
    return _query_df("SELECT * FROM programas_academicos", engine)


def cargar_materias_db(engine=None):
    if engine is None:
        engine = obtener_engine()
    return _query_df("SELECT * FROM materias", engine)


def cargar_grupos_db(engine=None):
    if engine is None:
        engine = obtener_engine()
    return _query_df("SELECT * FROM grupos", engine)


def cargar_matriculas_db(engine=None):
    if engine is None:
        engine = obtener_engine()
    return _query_df("SELECT * FROM matriculas", engine)


def cargar_calificaciones_db(engine=None):
    if engine is None:
        engine = obtener_engine()
    return _query_df("SELECT * FROM calificaciones", engine)


def cargar_administrativos_db(engine=None):
    if engine is None:
        engine = obtener_engine()
    query = """
        SELECT u.id, u.nombres, u.apellidos, u.correo, u.estado,
               NULL AS titulo_profesional, NULL AS especializacion, NULL AS foto
        FROM usuarios u
        WHERE u.rol IN ('ADMINISTRADOR', 'SUPER_ADMIN')
    """
    return _query_df(query, engine)


def cargar_todos_datos_db(engine=None):
    if engine is None:
        engine = obtener_engine()

    datos = {
        'estudiantes': cargar_estudiantes_db(engine),
        'profesores': cargar_profesores_db(engine),
        'administrativos': cargar_administrativos_db(engine),
        'programas_academicos': cargar_programas_academicos_db(engine),
        'materias': cargar_materias_db(engine),
        'grupos': cargar_grupos_db(engine),
        'matriculas': cargar_matriculas_db(engine),
        'calificaciones': cargar_calificaciones_db(engine),
    }
    print(f"Administrativos cargados: {len(datos['administrativos'])}")
    return datos
