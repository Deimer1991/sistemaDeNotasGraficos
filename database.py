import os
import re
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def _cargar_env(env_path=None):
    if env_path is None:
        env_path = Path(__file__).parent / ".env"
        if not env_path.exists():
            alt = Path(__file__).parent.parent / "proyectoIntegrador_Backend" / "sistemadenotas" / ".env"
            if alt.exists():
                env_path = alt
    
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ.setdefault(key.strip(), val.strip())


def obtener_engine():
    _cargar_env()

    jdbc_url = os.getenv("DB_URL")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")

    if not jdbc_url:
        raise ValueError("No se encontró DB_URL en el entorno ni en .env")

    m = re.match(r"jdbc:postgresql://([^:/]+):(\d+)/([^?]+)\??(.*)", jdbc_url)
    if not m:
        raise ValueError(f"No se pudo parsear DB_URL: {jdbc_url}")

    host = m.group(1)
    port = m.group(2)
    dbname = m.group(3)
    params = m.group(4)

    sslmode = "require"
    for param in params.split("&"):
        if param.startswith("sslmode="):
            sslmode = param.split("=", 1)[1]

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=username,
        password=password,
        host=host,
        port=int(port),
        database=dbname,
        query={"sslmode": sslmode},
    )

    return create_engine(url, pool_size=1, max_overflow=0, pool_pre_ping=True)


def ejecutar_query(query, engine=None):
    if engine is None:
        engine = obtener_engine()
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()


def obtener_columnas(query, engine=None):
    if engine is None:
        engine = obtener_engine()
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.keys()
