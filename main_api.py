import pandas as pd

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from carga import cargar_todos_datos_db
from analisis import (
    resumen_estadistico,
    promedio_por_estudiante,
    promedio_por_tipo_evaluacion,
    promedio_por_materia,
    promedio_por_grupo,
    ranking_estudiantes,
    estudiantes_bajo_desempeño,
    estudiantes_por_programa,
    estudiantes_por_semestre,
    ocupacion_grupos,
    materias_mas_demandadas,
    estudiantes_por_modalidad,
    carga_academica_profesores,
    estudiantes_por_profesor,
    desempeño_estudiantes_por_profesor,
    promedio_por_programa,
    matriculados_por_ano,
    filtrar_por_programa,
)

datos = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global datos
    print("Cargando datos desde PostgreSQL...")
    try:
        datos = cargar_todos_datos_db()
        print(f"Datos cargados: {len(datos['estudiantes'])} estudiantes, {len(datos['profesores'])} profesores, {len(datos['administrativos'])} administrativos")
    except Exception as e:
        print(f"Error cargando datos: {e}")
    yield


app = FastAPI(
    title="Analytics API - Sistema de Notas",
    description="API de análisis y estadísticas académicas",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _df_to_dict(df):
    if df is None or df.empty:
        return []
    return df.to_dict(orient="records")


# ============================================================================
# LISTAS PARA FILTROS
# ============================================================================

@app.get("/api/analytics/programas")
def listar_programas():
    df = datos["programas_academicos"][["id", "nombre"]]
    return _df_to_dict(df)


@app.get("/api/analytics/annos")
def listar_annos():
    df = datos["matriculas"].copy()
    df["ano"] = pd.to_datetime(df["fecha_matricula"]).dt.year
    annos = sorted(df["ano"].unique(), reverse=True)
    return [{"ano": int(a)} for a in annos]


# ============================================================================
# RESUMEN GENERAL
# ============================================================================

@app.get("/api/analytics/resumen")
def obtener_resumen():
    return resumen_estadistico(datos).to_dict()


# ============================================================================
# DESEMPEÑO ACADÉMICO
# ============================================================================

@app.get("/api/analytics/desempeno/estudiantes")
def obtener_promedio_estudiantes(top: int = Query(None, description="Limitar resultados"), programa_id: int = Query(None)):
    d = filtrar_por_programa(programa_id, datos)
    df = promedio_por_estudiante(d["calificaciones"], d["matriculas"], d["estudiantes"], d["programas_academicos"])
    if top:
        df = df.head(top)
    return _df_to_dict(df)


@app.get("/api/analytics/desempeno/tipos-evaluacion")
def obtener_promedio_tipos():
    df = promedio_por_tipo_evaluacion(datos["calificaciones"])
    return _df_to_dict(df.reset_index())


@app.get("/api/analytics/desempeno/materias")
def obtener_promedio_materias(programa_id: int = Query(None)):
    d = filtrar_por_programa(programa_id, datos)
    df = promedio_por_materia(d["calificaciones"], d["matriculas"], d["grupos"], d["materias"])
    return _df_to_dict(df.reset_index())


@app.get("/api/analytics/desempeno/grupos")
def obtener_promedio_grupos():
    df = promedio_por_grupo(datos["calificaciones"], datos["matriculas"], datos["grupos"], datos["materias"])
    return _df_to_dict(df.reset_index())


@app.get("/api/analytics/desempeno/ranking")
def obtener_ranking(programa_id: int = Query(None), top: int = Query(10)):
    d = filtrar_por_programa(programa_id, datos)
    ranking = ranking_estudiantes(d["calificaciones"], d["matriculas"], d["estudiantes"], d["programas_academicos"], top)
    return {
        "mejores": _df_to_dict(ranking["mejores"]),
        "peores": _df_to_dict(ranking["peores"]),
    }


@app.get("/api/analytics/desempeno/bajo-rendimiento")
def obtener_bajo_rendimiento(umbral: float = Query(3.0, description="Umbral de nota mínima"), programa_id: int = Query(None)):
    d = filtrar_por_programa(programa_id, datos)
    df = estudiantes_bajo_desempeño(d["calificaciones"], d["matriculas"], d["estudiantes"], umbral, d["programas_academicos"])
    return _df_to_dict(df)


@app.get("/api/analytics/desempeno/promedio-programas")
def obtener_promedio_programas(programa_id: int = Query(None)):
    d = filtrar_por_programa(programa_id, datos)
    df = promedio_por_programa(d["calificaciones"], d["matriculas"], d["estudiantes"], d["programas_academicos"])
    return _df_to_dict(df)


# ============================================================================
# DISTRIBUCIÓN
# ============================================================================

@app.get("/api/analytics/distribucion/programas")
def obtener_estudiantes_por_programa():
    df = estudiantes_por_programa(datos["estudiantes"], datos["programas_academicos"])
    return _df_to_dict(df)


@app.get("/api/analytics/distribucion/semestres")
def obtener_estudiantes_por_semestre():
    df = estudiantes_por_semestre(datos["matriculas"], datos["grupos"])
    return _df_to_dict(df)


@app.get("/api/analytics/distribucion/ocupacion-grupos")
def obtener_ocupacion_grupos(programa_id: int = Query(None)):
    d = filtrar_por_programa(programa_id, datos)
    df = ocupacion_grupos(d["matriculas"], d["grupos"])
    return _df_to_dict(df)


@app.get("/api/analytics/distribucion/materias-demandadas")
def obtener_materias_demandadas():
    df = materias_mas_demandadas(datos["matriculas"], datos["grupos"], datos["materias"])
    return _df_to_dict(df)


@app.get("/api/analytics/distribucion/modalidad")
def obtener_estudiantes_por_modalidad(programa_id: int = Query(None)):
    d = filtrar_por_programa(programa_id, datos)
    df = estudiantes_por_modalidad(d["estudiantes"], d["programas_academicos"])
    return _df_to_dict(df)


@app.get("/api/analytics/distribucion/matriculados-ano")
def obtener_matriculados_ano(programa_id: int = Query(None)):
    d = filtrar_por_programa(programa_id, datos)
    df = matriculados_por_ano(d["matriculas"])
    return _df_to_dict(df)


# ============================================================================
# PROFESORES
# ============================================================================

@app.get("/api/analytics/profesores/carga-academica")
def obtener_carga_academica():
    df = carga_academica_profesores(datos["grupos"], datos["profesores"])
    return _df_to_dict(df)


@app.get("/api/analytics/profesores/estudiantes")
def obtener_estudiantes_por_profesor():
    df = estudiantes_por_profesor(datos["matriculas"], datos["grupos"], datos["profesores"])
    return _df_to_dict(df)


@app.get("/api/analytics/profesores/desempeno")
def obtener_desempeno_por_profesor(programa_id: int = Query(None)):
    d = filtrar_por_programa(programa_id, datos)
    df = desempeño_estudiantes_por_profesor(d["calificaciones"], d["matriculas"], d["grupos"], d["profesores"])
    return _df_to_dict(df)


# ============================================================================
# RECARGAR DATOS (refresca desde BD)
# ============================================================================

@app.post("/api/analytics/recargar")
def recargar_datos():
    global datos
    try:
        datos = cargar_todos_datos_db()
        return {
            "status": "ok",
            "estudiantes": len(datos.get("estudiantes", [])),
            "profesores": len(datos.get("profesores", [])),
            "administrativos": len(datos.get("administrativos", [])),
            "programas": len(datos.get("programas_academicos", [])),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/api/analytics/health")
def health():
    return {
        "status": "ok",
        "estudiantes": len(datos.get("estudiantes", [])),
        "profesores": len(datos.get("profesores", [])),
        "calificaciones": len(datos.get("calificaciones", [])),
    }
