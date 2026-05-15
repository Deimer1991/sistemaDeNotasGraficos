import random
import uuid
from datetime import datetime, timedelta
from database import obtener_engine
from sqlalchemy import text

random.seed(42)

# ============================================================================
# DATOS DE REFERENCIA
# ============================================================================

NOMBRES_MASC = [
    "Carlos", "Andrés", "Miguel", "Jorge", "Felipe", "Luis", "Juan", "David",
    "Santiago", "Pablo", "Diego", "Javier", "Fernando", "Cristian", "Manuel",
    "Alejandro", "Ricardo", "Oscar", "Daniel", "Pedro", "Camilo", "Iván",
    "Esteban", "Hugo", "Gabriel", "Tomás", "Martín", "Mateo", "Emilio", "Maximiliano",
    "Leonardo", "Adrián", "Sergio", "Julian", "Mauricio", "Raúl", "Gustavo",
    "Alberto", "Francisco", "Eduardo", "Vicente", "Marco", "Fabián", "Héctor",
    "Arturo", "Rafael", "Ignacio", "Rodrigo", "Lucas", "Benjamín",
]

NOMBRES_FEM = [
    "María", "Laura", "Camila", "Valentina", "Carolina", "Andrea", "Daniela",
    "Paula", "Sofía", "Isabella", "Luisa", "Ana", "Gabriela", "Natalia",
    "Tatiana", "Diana", "Mónica", "Adriana", "Liliana", "Rosa", "Elena",
    "Angélica", "Viviana", "Alejandra", "Juliana", "Fernanda", "Claudia",
    "Marcela", "Pilar", "Margarita", "Manuela", "Sara", "Mariana", "Ximena",
    "Lorena", "Verónica", "Patricia", "Gloria", "Martha", "Lucía",
    "Catherine", "Johanna", "Lina", "Mayra", "Raquel", "Beatriz", "Estefanía",
    "Jessica", "Katherine", "Nicolle",
]

APELLIDOS = [
    "García", "Rodríguez", "Martínez", "López", "González", "Pérez", "Sánchez",
    "Ramírez", "Cruz", "Flores", "Morales", "Ortiz", "Vargas", "Castro",
    "Torres", "Gómez", "Reyes", "Herrera", "Medina", "Mendoza", "Álvarez",
    "Castillo", "Romero", "Moreno", "Rojas", "Jiménez", "Ruiz", "Díaz",
    "Silva", "Delgado", "Peña", "Contreras", "Molina", "Aguilar", "Cordero",
    "Paredes", "Cabrera", "Campos", "Rivera", "Acosta", "Cárdenas", "Rivas",
    "Salazar", "Chávez", "Vega", "Figueroa", "León", "Vásquez", "Soto",
    "Muñoz", "Garrido", "Guerrero", "Miranda", "Valencia", "Espinoza",
]

PROGRAMAS = [
    ("Ingeniería de Sistemas", "Presencial"),
    ("Medicina", "Presencial"),
    ("Administración de Empresas", "Virtual"),
    ("Derecho", "Presencial"),
    ("Psicología", "Virtual"),
    ("Arquitectura", "Presencial"),
    ("Contaduría Pública", "Virtual"),
    ("Biología Marina", "Presencial"),
]

MATERIAS_POR_PROGRAMA = {
    "Ingeniería de Sistemas": [
        "Programación I", "Estructuras de Datos", "Bases de Datos", "Redes de Computadores", "Ingeniería de Software"
    ],
    "Medicina": [
        "Anatomía Humana", "Fisiología", "Farmacología", "Patología", "Semiología"
    ],
    "Administración de Empresas": [
        "Contabilidad General", "Marketing", "Finanzas Corporativas", "Gestión del Talento Humano", "Economía General"
    ],
    "Derecho": [
        "Derecho Constitucional", "Derecho Penal", "Derecho Civil", "Derecho Laboral", "Derecho Comercial"
    ],
    "Psicología": [
        "Psicología General", "Psicología Clínica", "Neuropsicología", "Psicología Social", "Psicología del Desarrollo"
    ],
    "Arquitectura": [
        "Dibujo Arquitectónico", "Historia de la Arquitectura", "Diseño Estructural", "Urbanismo", "Materiales y Construcción"
    ],
    "Contaduría Pública": [
        "Contabilidad Financiera", "Auditoría", "Impuestos", "Costos y Presupuestos", "Contabilidad Internacional"
    ],
    "Biología Marina": [
        "Oceanografía", "Biología Molecular", "Ecología Acuática", "Zoología Marina", "Botánica Marina"
    ],
}

TODAS_MATERIAS = []
for prog, mats in MATERIAS_POR_PROGRAMA.items():
    for m in mats:
        TODAS_MATERIAS.append((m, prog))

TITULOS_PROFESIONALES = [
    "Ingeniero de Sistemas", "Médico Cirujano", "Administrador de Empresas",
    "Abogado", "Psicólogo", "Arquitecto", "Contador Público", "Biólogo Marino",
    "Magíster en Educación", "Doctor en Ciencias", "Especialista en Docencia",
    "Magíster en Investigación"
]

TIPOS_DOCUMENTO = ["CC", "CE", "TI"]

TIPO_EVAL = ["PARCIAL_1", "PARCIAL_2", "TRABAJO", "EXAMEN_FINAL"]

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def nombre_aleatorio():
    return random.choice(NOMBRES_MASC + NOMBRES_FEM)

def apellido_aleatorio():
    return f"{random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"

def email_aleatorio(nombres, apellidos):
    ap = apellidos.split()[0].lower()
    ap = ap.replace(" ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    nm = nombres.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    dominios = ["email.com", "correo.com", "estudiante.edu.co", "profesor.edu.co", "outlook.com", "gmail.com"]
    return f"{nm}.{ap}{random.randint(1, 999)}@{random.choice(dominios)}"

def celular_aleatorio():
    return f"3{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"

def token_unico():
    return str(uuid.uuid4())

def nota_aleatoria():
    return round(random.uniform(1.0, 5.0), 1)

def fecha_aleatoria(start_year=2024, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

BCRYPT_HASH = "$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy"

# ============================================================================
# INSERCIÓN
# ============================================================================

def _batch_insert(conn, table, columns, values, returning=False):
    if not values:
        return []
    cols = ", ".join(columns)
    batch = []
    ids = []
    for row in values:
        batch.append(row)
        if len(batch) >= 500:
            _do_batch(conn, table, cols, columns, batch, returning, ids)
            batch = []
    if batch:
        _do_batch(conn, table, cols, columns, batch, returning, ids)
    return ids


def _do_batch(conn, table, cols, columns, batch, returning, ids):
    vals_list = []
    flat = {}
    for idx, r in enumerate(batch):
        phs = ", ".join([f":r{idx}_{c}" for c in columns])
        vals_list.append(f"({phs})")
        for k, v in r.items():
            flat[f"r{idx}_{k}"] = v
    vals = ", ".join(vals_list)
    sql = f"INSERT INTO {table} ({cols}) VALUES {vals}"
    if returning:
        sql += " RETURNING id"
        ids.extend(r[0] for r in conn.execute(text(sql), flat).fetchall())
    else:
        conn.execute(text(sql), flat)


def main():
    engine = obtener_engine()
    print("Conectado a la base de datos.")

    with engine.begin() as conn:
        # ====================================================================
        # 1. PROGRAMAS ACADÉMICOS
        # ====================================================================
        print("\n1. Insertando programas académicos...")
        prog_ids = {}
        for nombre, modalidad in PROGRAMAS:
            r = conn.execute(
                text("""
                    INSERT INTO programas_academicos (nombre, descripcion, modalidad, estado, fecha_creacion)
                    VALUES (:nombre, :desc, :modalidad, 'ACTIVO', :fecha)
                    RETURNING id
                """),
                {"nombre": nombre, "desc": f"Programa de {nombre}", "modalidad": modalidad, "fecha": fecha_aleatoria()}
            ).fetchone()
            prog_ids[nombre] = r[0]
        print(f"  → {len(PROGRAMAS)} programas insertados.")

        # ====================================================================
        # 2. MATERIAS
        # ====================================================================
        print("2. Insertando materias...")
        mat_ids = {}
        for nombre, prog in TODAS_MATERIAS:
            r = conn.execute(
                text("""
                    INSERT INTO materias (nombre, estado)
                    VALUES (:nombre, 'ACTIVO')
                    RETURNING id
                """),
                {"nombre": nombre}
            ).fetchone()
            mat_ids[nombre] = r[0]
        print(f"  → {len(TODAS_MATERIAS)} materias insertadas.")

        # ====================================================================
        # 3. PROGRAMA_MATERIA
        # ====================================================================
        print("3. Insertando relación programa-materia...")
        pm_count = 0
        for prog_name, materias in MATERIAS_POR_PROGRAMA.items():
            pid = prog_ids[prog_name]
            for mat_name in materias:
                mid = mat_ids[mat_name]
                try:
                    conn.execute(
                        text("""
                            INSERT INTO programa_materia (programa_id, materia_id)
                            VALUES (:pid, :mid)
                        """),
                        {"pid": pid, "mid": mid}
                    )
                    pm_count += 1
                except Exception:
                    pass
        print(f"  → {pm_count} relaciones insertadas.")

        # ====================================================================
        # 4. USUARIOS (1000 total)
        # ====================================================================
        print("4. Insertando 1000 usuarios...")
        docs_generated = set()
        emails_generated = set()
        usuarios_data = []

        for i in range(1000):
            nombres = nombre_aleatorio()
            apellidos = apellido_aleatorio()
            doc = str(random.randint(1000000, 99999999))
            while doc in docs_generated:
                doc = str(random.randint(1000000, 99999999))
            docs_generated.add(doc)
            email = email_aleatorio(nombres, apellidos)
            while email in emails_generated:
                email = email_aleatorio(nombres, apellidos)
            emails_generated.add(email)

            if i == 0:
                rol = "SUPER_ADMIN"
            elif 1 <= i <= 10:
                rol = "ADMINISTRADOR"
            elif 11 <= i <= 40:
                rol = "PROFESOR"
            else:
                rol = "ESTUDIANTE"

            usuarios_data.append({
                "nombres": nombres,
                "apellidos": apellidos,
                "tipo_documento": random.choice(TIPOS_DOCUMENTO),
                "documento": doc,
                "correo": email,
                "numero_celular": celular_aleatorio(),
                "contraseña": BCRYPT_HASH,
                "rol": rol,
                "estado": "ACTIVO",
                "envio_correo": "ENVIADO",
                "token_registro": token_unico(),
                "registro": "COMPLETO",
                "token_recuperacion": None,
                "expiracion_token_recuperacion": None,
                "fecha_registro": fecha_aleatoria(),
                "fecha_actualizacion": fecha_aleatoria(),
            })

        user_ids = _batch_insert(
            conn, "usuarios",
            ["nombres", "apellidos", "tipo_documento", "documento", "correo", "numero_celular",
             "contraseña", "rol", "estado", "envio_correo", "token_registro", "registro",
             "token_recuperacion", "expiracion_token_recuperacion", "fecha_registro", "fecha_actualizacion"],
            usuarios_data, returning=True
        )
        print(f"  → {len(user_ids)} usuarios insertados.")

        # ====================================================================
        # 5. TABLAS HIJAS
        # ====================================================================
        print("5. Insertando tablas hijas...")

        admin_ids = user_ids[:11]
        prof_ids = user_ids[11:41]
        est_ids = user_ids[41:]

        admin_vals = [{"id_usuario": uid, "titulo": random.choice(TITULOS_PROFESIONALES),
                       "especializacion": random.choice(["Gestión Educativa", "Administración Pública", "Finanzas", "Recursos Humanos", "Dirección de proyectos"])}
                      for uid in admin_ids]
        _batch_insert(conn, "administrativos", ["id_usuario", "titulo", "especializacion"], admin_vals)
        print(f"  → {len(admin_ids)} administrativos insertados.")

        prof_vals = [{"id_usuario": uid,
                      "titulo": random.choice(TITULOS_PROFESIONALES),
                      "especializacion": random.choice(["Docencia Universitaria", "Investigación", "Currículo",
                                                         "Evaluación Educativa", "Tecnología Educativa", "Pedagogía"])}
                     for uid in prof_ids]
        _batch_insert(conn, "profesores", ["id_usuario", "titulo", "especializacion"], prof_vals)
        print(f"  → {len(prof_ids)} profesores insertados.")

        prog_names = [p[0] for p in PROGRAMAS]
        est_vals = [{"id_usuario": uid, "programa_id": prog_ids[random.choice(prog_names)]}
                    for uid in est_ids]
        _batch_insert(conn, "estudiantes", ["id_usuario", "programa_id"], est_vals)
        print(f"  → {len(est_ids)} estudiantes insertados.")

        # ====================================================================
        # 6. GRUPOS
        # ====================================================================
        print("6. Insertando grupos...")
        grupo_ids = []
        letras = "ABCDEFGH"

        for mat_name, mid in mat_ids.items():
            for sem in ["2026-1", "2026-2"]:
                prof_id = random.choice(prof_ids)
                cupo = random.randint(30, 45)
                nombre = f"{mat_name[:15]} {random.choice(letras)}"
                try:
                    r = conn.execute(
                        text("""
                            INSERT INTO grupos (nombre, semestre, cupo_maximo, estado, materia_id, profesor_id)
                            VALUES (:nombre, :sem, :cupo, 'ACTIVO', :mid, :pid)
                            RETURNING id
                        """),
                        {"nombre": nombre, "sem": sem, "cupo": cupo, "mid": mid, "pid": prof_id}
                    ).fetchone()
                    grupo_ids.append(r[0])
                except Exception:
                    pass
        print(f"  → {len(grupo_ids)} grupos insertados.")

        # ====================================================================
        # 7. MATRÍCULAS (batch con RETURNING)
        # ====================================================================
        print("7. Insertando matrículas...")
        matricula_rows_all = []
        matricula_batch = []

        for est_id in est_ids:
            grupos_inscritos = random.sample(grupo_ids, min(5, len(grupo_ids)))
            for gid in grupos_inscritos:
                matricula_batch.append({
                    "grupo_id": gid,
                    "estudiante_id": est_id,
                    "fecha_matricula": fecha_aleatoria(2025, 2026),
                    "estado": "ACTIVO",
                })
                if len(matricula_batch) >= 500:
                    ids = _batch_insert(conn, "matriculas",
                        ["grupo_id", "estudiante_id", "fecha_matricula", "estado"],
                        matricula_batch, returning=True)
                    matricula_rows_all.extend(ids)
                    matricula_batch = []

        if matricula_batch:
            ids = _batch_insert(conn, "matriculas",
                ["grupo_id", "estudiante_id", "fecha_matricula", "estado"],
                matricula_batch, returning=True)
            matricula_rows_all.extend(ids)

        print(f"  → {len(matricula_rows_all)} matrículas insertadas.")

        if not matricula_rows_all:
            print("  ⚠ No hay matrículas, se omiten calificaciones.")
            return

        # ====================================================================
        # 8. CALIFICACIONES (batch)
        # ====================================================================
        print("8. Insertando calificaciones...")
        cal_batch = []
        cal_count = 0

        for mid in matricula_rows_all:
            for momento in [1, 2]:
                for tipo in TIPO_EVAL:
                    cal_batch.append({
                        "matricula_id": mid,
                        "momento": momento,
                        "tipo": tipo,
                        "nota": nota_aleatoria(),
                    })
                    if len(cal_batch) >= 500:
                        _batch_insert(conn, "calificaciones",
                            ["matricula_id", "momento", "tipo", "nota"], cal_batch)
                        cal_count += len(cal_batch)
                        cal_batch = []

        if cal_batch:
            _batch_insert(conn, "calificaciones",
                ["matricula_id", "momento", "tipo", "nota"], cal_batch)
            cal_count += len(cal_batch)

        print(f"  → {cal_count} calificaciones insertadas.")

    print("\n" + "=" * 60)
    print("✅ INSERCIÓN MASIVA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print(f"\nResumen final:")
    print(f"  Programas:           {len(PROGRAMAS)}")
    print(f"  Materias:            {len(TODAS_MATERIAS)}")
    print(f"  Relaciones Prog-Mat: {pm_count}")
    print(f"  Usuarios:            {len(user_ids)}")
    print(f"  - SUPER_ADMIN:       {1}")
    print(f"  - Administrativos:   {10}")
    print(f"  - Profesores:        {30}")
    print(f"  - Estudiantes:       {959}")
    print(f"  Grupos:              {len(grupo_ids)}")
    print(f"  Matrículas:          {len(matricula_rows_all)}")
    print(f"  Calificaciones:      {cal_count}")


if __name__ == "__main__":
    main()
