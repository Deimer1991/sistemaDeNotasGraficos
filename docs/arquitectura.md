# Arquitectura del Sistema de Notas

> Documento técnico completo - Arquitectura de 3 capas

---

## 1. Visión General (3 Capas)

```
+-----------------------------------------------------+
|              REACT FRONTEND (Vite 8)                 |
|           http://localhost:5175                       |
|  +-----------+-----------+-----------+-----------+  |
|  | Landing   |  Login    |  Register | AdmonMain |  |
|  | Dashboard | Dashboard | Comple-   | Analytics |  |
|  | Estudiante| Profesor  | tar Forms | Dashboard |  |
|  +-----------+-----------+-----------+-----------+  |
+---------------------------+-------------------------+
                            |
              +-------------+-------------+
              |                           |
        fetch() directo              Axios (con JWT)
      (toda la app excepto        (solo analytics)
            analytics)                  |
              |                          |
+-------------v-----------+  +----------v--------------+
|    JAVA SPRING BOOT 4   |  | PYTHON FASTAPI 0.115   |
|   http://localhost:8081  |  | http://localhost:8000   |
|                          |  |                         |
|  CRUD + Auth + Email     |  | Analytics in-memory     |
|  11 Controllers          |  | 20 endpoints GET        |
|  12 Services             |  | 1 endpoint POST         |
|  10 Repositories         |  |   (/recargar)           |
|  10 Entities (JPA/Hib.)  |  | Pandas DataFrames       |
+-------------+------------+  +-------------------------+
              |
              | JDBC (Hibernate / psycopg2)
              |
+-------------v---------------------------------------+
|            POSTGRESQL (db.prisma.io:5432)           |
|                                                      |
|  10 tablas: usuarios, estudiantes, profesores,      |
|  administrativos, programas_academicos, materias,   |
|  programa_materia, grupos, matriculas,              |
|  calificaciones                                     |
+------------------------------------------------------+
```

### Tecnologías Principales

| Capa | Tecnología | Versión | Puerto |
|------|-----------|---------|--------|
| Frontend | React + Vite + Tailwind | React 19 / Vite 8 | 5175 |
| Backend CRUD | Java Spring Boot | 4.0.3 | 8081 |
| Backend Analytics | Python FastAPI | 0.115.6 | 8000 |
| Base de Datos | PostgreSQL | - | 5432 |

---

## 2. React Frontend

### Ubicación
```
C:\Users\ASUS VIVOBook\Desktop\ProyectoIntegradorFrontend\Practica\src\
```

### Frameworks y Librerías

| Librería | Uso |
|----------|-----|
| React 19 | UI, estado, hooks |
| Vite 8 | Build tool, dev server (HMR) |
| react-router-dom 7 | Routing (BrowserRouter, Outlet, useNavigate, useLocation) |
| Tailwind CSS 4 | Estilos utility-first |
| Recharts 2 | Gráficos (PieChart, BarChart) |
| Axios | HTTP al Python backend (analytics) |
| Lucide React | Iconos |
| framer-motion 11 | Animaciones |

### Páginas y Datos que Consumen

| Ruta | Componente | Consume a | Endpoints |
|------|-----------|-----------|-----------|
| `/` | LandingPage | Ninguno | Todo UI estático |
| `/login` | Login | Java | `POST /api/auth/login`, `POST /api/recuperacion/solicitar` |
| `/registrar` | Register | Java | `POST /api/usuarios` |
| `/admonMain` | AdmonMain | Java + Python | ~25 endpoints CRUD + `POST /recargar` |
| `/analytics` | AnalyticsDashboard | Python | 5 endpoints analytics |
| `/dashboard/estudiante` | EstudianteDashboard | Java | perfil, matrículas, calificaciones |
| `/dashboard/profesor` | ProfesorDashboard | Java | grupos, matrículas, calificaciones |
| `/completar/estudiante/:token` | FormEstudiante | Java | usuario por token, programas activos |
| `/completar/profesor/:token` | FormProfesor | Java | usuario por token, crear profesor |
| `/completar/administrador/:token` | FormAdministrador | Java | usuario por token, crear admin |
| `/recuperar-contrasena/:token` | RecuperarContrasena | Java | validar/cambiar contraseña |

### Dos Mecanismos HTTP

**1. `fetch()` directo hacia Java (localhost:8081)**
- Usado en: todas las páginas excepto AnalyticsDashboard
- El token JWT se adjunta manualmente: `Authorization: Bearer ${token}`
- Las URLs están hardcodeadas en cada componente

**2. Axios hacia Python (localhost:8000)**
- Usado solo en: AnalyticsDashboard (a través de hooks)
- Base URL configurable: `import.meta.env.VITE_API_URL || "http://localhost:8000"`
- Interceptor: adjunta token JWT automáticamente
- Interceptor: en 401 redirige a `/login`

### Hooks Personalizados (useAnalytics.js)

Todos los hooks siguen el patrón `useAnalyticsData(fetchFn, deps)` y retornan `{ data, loading, error, refetch }`.

| Hook | Endpoint Python | Parámetros |
|------|----------------|------------|
| useResumen | `GET /resumen` | refreshKey |
| useDistribucionProgramas | `GET /distribucion/programas` | refreshKey |
| useModalidad | `GET /distribucion/modalidad` | filters, refreshKey |
| useRanking | `GET /desempeno/ranking` | filters, refreshKey |
| useProgramasList | `GET /programas` | refreshKey |
| useDesempenoMaterias | `GET /desempeno/materias` | filters, refreshKey |
| usePromedioProgramas | `GET /desempeno/promedio-programas` | filters, refreshKey |
| useMatriculadosAno | `GET /distribucion/matriculados-ano` | filters, refreshKey |
| useOcupacionGrupos | `GET /distribucion/ocupacion-grupos` | filters, refreshKey |
| useProfesoresDesempeno | `GET /profesores/desempeno` | filters, refreshKey |

### Layouts

- **MainLayout**: Navbar + Outlet + Footer (para páginas públicas: Landing, Login, Register)
- **AuthLayout**: Solo Outlet (para páginas autenticadas)
- **Sin Layout**: FormEstudiante, FormProfesor, FormAdministrador (llegan por email)

---

## 3. Java Spring Boot Backend

### Ubicación
```
C:\Users\ASUS VIVOBook\Desktop\proyectoIntegrador_Backend\sistemadenotas\
```

### Arquitectura por Capas

```
Controller → Service → Repository → Entity → PostgreSQL
     ↑
 DTOs (Data Transfer Objects)
```

### Controllers (11) y sus Endpoints

| Controller | Base Path | Endpoints |
|-----------|-----------|-----------|
| AuthController | `/api/auth` | `POST /login` |
| UsuarioController | `/api/usuarios` | `POST /` (crear), `GET /` (listar DTO), `PUT /{id}/rol`, `POST /{id}/enviar-correo`, `GET /token/{token}` |
| EstudianteController | `/api/estudiantes` | `POST /`, `GET /{id}`, `PUT /{id}`, `GET /` |
| ProfesorController | `/api/profesores` | `POST /`, `GET /{id}`, `PUT /{id}`, `GET /` |
| AdministradorController | `/api/administradores` | `POST /`, `GET /{id}`, `PUT /{id}` |
| ProgramaAcademicoController | `/api/programas` | `GET /activos`, `GET /`, `POST /`, `PUT /{id}`, `DELETE /{id}` |
| MateriaController | `/api/materias` | `GET /`, `GET /activas`, `POST /`, `PUT /{id}`, `DELETE /{id}`, `GET /programa/{id}`, `POST /programa/{pid}/asignar/{mid}`, `DELETE /programa/{pid}/quitar/{mid}` |
| GrupoController | `/api/grupos` | `GET /`, `GET /activos`, `GET /profesor/{id}`, `GET /{id}`, `POST /`, `PUT /{id}`, `DELETE /{id}`, `PUT /{id}/activar` |
| MatriculaController | `/api/matriculas` | `GET /`, `GET /grupo/{id}`, `GET /estudiante/{id}`, `POST /`, `DELETE /{id}` |
| CalificacionController | `/api/calificaciones` | `GET /matricula/{id}`, `GET /grupo/{id}`, `POST /`, `GET /matricula/{id}/nota-final` |
| RecuperacionController | `/api/recuperacion` | `POST /solicitar`, `GET /validar/{token}`, `POST /cambiar` |

### Services (12) - Lógica de Negocio

| Service | Responsabilidad |
|---------|----------------|
| JwtService | Generar/validar tokens JWT (HMAC-SHA, 24h) |
| EmailService | Enviar correos (Gmail SMTP) para registro y recuperación |
| UsuarioService | CRUD usuarios, primer usuario = SUPER_ADMIN, asignar roles |
| EstudianteService | Completar registro (asignar programa), actualizar perfil |
| ProfesorService | Completar registro (título, especialización) |
| AdministradorService | Completar registro admin |
| ProgramaAcademicoService | CRUD programas (soft-delete: estado INACTIVO) |
| MateriaService | CRUD materias + asignación a programas |
| GrupoService | CRUD grupos (activar/desactivar) |
| MatriculaService | Matricular/retirar estudiantes |
| CalificacionService | Registrar notas (validación 0.0-5.0), calcular promedios ponderados |
| RecuperacionService | Tokens de recuperación (1h expiración) |

### Sistema de Calificaciones

3 momentos académicos (M1, M2, M3):

**Ponderación por momento:**
- PARCIAL_1: 20%
- PARCIAL_2: 20%
- TRABAJO: 20%
- EXAMEN_FINAL: 40%

**Nota final:** M1 × 30% + M2 × 30% + M3 × 40%

### Entities (10)

| Entidad | Tabla | Extiende de |
|---------|-------|-------------|
| Usuario | usuarios | (base, JOINED) |
| Estudiante | estudiantes | Usuario (id_usuario) |
| Profesor | profesores | Usuario (id_usuario) |
| Administrador | administrativos | Usuario (id_usuario) |
| ProgramaAcademico | programas_academicos | - |
| Materia | materias | - |
| ProgramaMateria | programa_materia | (junction) |
| Grupo | grupos | - |
| Matricula | matriculas | - |
| Calificacion | calificaciones | - |

### Configuración

| Propiedad | Valor |
|-----------|-------|
| Server port | 8081 |
| DB URL | `jdbc:postgresql://db.prisma.io:5432/postgres?sslmode=require` |
| JPA DDL | `update` (Hibernate gestiona esquema) |
| JWT Secret | `clave-super-secreta-sistema-de-notas-2026-debe-ser-larga` |
| JWT Expiración | 86400000ms (24h) |
| CORS Origins | localhost:5173, 5174, 5175 |

**⚠️ Seguridad:** Aunque JWT se genera en login, **no hay filtro de seguridad** que valide el token. Todos los endpoints están con `.anyRequest().permitAll()`.

---

## 4. Python FastAPI Backend

### Ubicación
```
C:\Users\ASUS VIVOBook\Desktop\sistema-notas\
```

### Archivos del Proyecto

| Archivo | Líneas | Rol |
|---------|--------|-----|
| main_api.py | 246 | Servidor FastAPI (endpoints) |
| main.py | 72 | CLI offline (reportes por consola) |
| database.py | 75 | Conexión PostgreSQL (SQLAlchemy) |
| carga.py | 164 | Carga de datos (BD + archivos) |
| analisis.py | 225 | Funciones de análisis (pandas) |
| limpieza.py | 160 | Validación de calidad de datos |
| reportes.py | 263 | Generación de reportes TXT/CSV |
| grafico.py | 51 | Gráficos standalone (no usado) |
| seed_data.py | 424 | Generador de datos sintéticos |

### Endpoints (21)

| Método | Ruta | Parámetros | Descripción |
|--------|------|-----------|-------------|
| GET | `/api/analytics/programas` | - | Lista programas (id + nombre) |
| GET | `/api/analytics/annos` | - | Años distintos de matrículas |
| GET | `/api/analytics/resumen` | - | Conteo de entidades activas |
| GET | `/api/analytics/desempeno/estudiantes` | top, programa_id | Promedio por estudiante |
| GET | `/api/analytics/desempeno/tipos-evaluacion` | - | Promedio por tipo de evaluación |
| GET | `/api/analytics/desempeno/materias` | programa_id | Promedio por materia |
| GET | `/api/analytics/desempeno/grupos` | - | Promedio por grupo |
| GET | `/api/analytics/desempeno/ranking` | top, programa_id | Mejores y peores estudiantes |
| GET | `/api/analytics/desempeno/bajo-rendimiento` | umbral, programa_id | Estudiantes bajo umbral |
| GET | `/api/analytics/desempeno/promedio-programas` | programa_id | Promedio por programa |
| GET | `/api/analytics/distribucion/programas` | - | Cantidad estudiantes por programa |
| GET | `/api/analytics/distribucion/semestres` | - | Cantidad por semestre |
| GET | `/api/analytics/distribucion/ocupacion-grupos` | programa_id | Ocupación vs capacidad |
| GET | `/api/analytics/distribucion/materias-demandadas` | - | Materias más cursadas |
| GET | `/api/analytics/distribucion/modalidad` | programa_id | Distribución por modalidad |
| GET | `/api/analytics/distribucion/matriculados-ano` | programa_id | Matriculados por año |
| GET | `/api/analytics/profesores/carga-academica` | - | Grupos por profesor |
| GET | `/api/analytics/profesores/estudiantes` | - | Estudiantes por profesor |
| GET | `/api/analytics/profesores/desempeno` | programa_id | Promedio estudiantes por profesor |
| POST | `/api/analytics/recargar` | - | Recargar datos desde BD |
| GET | `/api/analytics/health` | - | Health check |

### Flujo de Datos en Memoria

```
[PostgreSQL]
     ↓ (8 consultas SQL al iniciar)
cargar_todos_datos_db()
     ↓
datos = {
    estudiantes: DataFrame,      ← 959+ registros
    profesores: DataFrame,       ← 30 registros
    administrativos: DataFrame,  ← 10+ registros
    programas_academicos: DataFrame,
    materias: DataFrame,
    grupos: DataFrame,
    matriculas: DataFrame,       ← miles
    calificaciones: DataFrame    ← decenas de miles
}
     ↓
[EN MEMORIA durante toda la ejecución]
     ↓
Por cada petición:
  1. Opcional: filtrar_por_programa() subconjunto
  2. Operaciones pandas (merge, groupby, agg, sort)
  3. _df_to_dict() → JSON
  4. Respuesta al cliente
```

### Carga de Datos (carga.py)

8 funciones que ejecutan SQL vía `pd.read_sql_query()`:

| Función | Query |
|---------|-------|
| cargar_estudiantes_db() | SELECT usuarios JOIN estudiantes WHERE rol='ESTUDIANTE' |
| cargar_profesores_db() | SELECT usuarios JOIN profesores WHERE rol='PROFESOR' |
| cargar_administrativos_db() | SELECT usuarios JOIN administrativos WHERE rol IN ('ADMINISTRADOR','SUPER_ADMIN') |
| cargar_programas_academicos_db() | SELECT * FROM programas_academicos |
| cargar_materias_db() | SELECT * FROM materias |
| cargar_grupos_db() | SELECT * FROM grupos |
| cargar_matriculas_db() | SELECT * FROM matriculas |
| cargar_calificaciones_db() | SELECT * FROM calificaciones |

---

## 5. ¿Quién consume a quién?

| Desde | Hacia | Puerto | Protocolo | ¿Qué intercambian? |
|-------|-------|--------|-----------|-------------------|
| React (fetch) | Java | 8081 | HTTP/REST | CRUD completo: auth, usuarios, programas, materias, grupos, matrículas, calificaciones |
| React (Axios) | Python | 8000 | HTTP/REST | Datos de analytics: estadísticas, distribuciones, rankings |
| Java (JPA/Hibernate) | PostgreSQL | 5432 | JDBC | Persistencia y consultas ORM |
| Python (pandas) | PostgreSQL | 5432 | SQL (read_sql) | Lectura de datos al startup y en recargar |

**Java y Python NO se comunican directamente.** Ambos acceden a la misma BD. Java escribe, Python lee. Para sincronizar, se llama a `POST /api/analytics/recargar`.

---

## 6. Flujo de Autenticación

```
1. React (Login) → POST /api/auth/login { correo, contraseña }
2. Java AuthController → JwtService → UsuarioRepository.findByCorreo()
3. Java responde: { token, rol, id, nombres, apellidos }
4. React guarda en localStorage: token, rol, id, nombres, apellidos
5. Llamadas posteriores:
   - fetch(): header manual Authorization: Bearer <token>
   - Axios: interceptor automático
```

---

## 7. Esquema de Base de Datos

```
usuarios
├── id (PK, auto increment)
├── nombres, apellidos (NombreCompleto embeddable)
├── tipo_documento, documento
├── correo (único)
├── contraseña
├── rol (ESTUDIANTE|PROFESOR|ADMINISTRADOR|SUPER_ADMIN)
├── estado (ACTIVO|INACTIVO)
├── envio_correo (ENVIADO|NO_ENVIADO)
├── token_registro (único)
├── registro (PENDIENTE|COMPLETO)
├── token_recuperacion
├── expiracion_token_recuperacion

estudiantes (hereda de usuarios vía id_usuario)
├── programa_id → programas_academicos

profesores (hereda de usuarios vía id_usuario)
├── titulo_profesional, especializacion, foto

administrativos (hereda de usuarios vía id_usuario)
├── titulo_profesional, especializacion, foto

programas_academicos
├── id, nombre, descripcion, modalidad, estado, fecha_creacion

materias
├── id, nombre (único), estado

programa_materia (junction)
├── id, programa_id → programas, materia_id → materias
├── UNIQUE(programa_id, materia_id)

grupos
├── id, nombre, semestre, cupo_maximo, estado
├── materia_id → materias, profesor_id → profesores

matriculas
├── id, grupo_id, estudiante_id, fecha_matricula, estado
├── UNIQUE(grupo_id, estudiante_id)

calificaciones
├── id, matricula_id, momento (1-3), tipo (PARCIAL_1|PARCIAL_2|TRABAJO|EXAMEN_FINAL), nota (0.0-5.0)
├── UNIQUE(matricula_id, momento, tipo)
```

---

## 8. Ejemplo: Flujo Completo "Desactivar Programa → Actualizar Tarjetas"

```
1. Admin hace clic en "Desactivar" en tabla de programas (AdmonMain)
     ↓
2. → fetch('DELETE http://localhost:8081/api/programas/{id}')
     ↓
3. Java (ProgramaAcademicoService.eliminar):
   - programa.setEstado("INACTIVO")
   - programaRepository.save(programa)
     ↓
4. React actualiza estado local del programa
     ↓
5. → fetch('POST http://localhost:8000/api/analytics/recargar')
     ↓
6. Python recarga todas las consultas SQL desde PostgreSQL
   - datos = cargar_todos_datos_db()  ← datos frescos
     ↓
7. React: setRefreshKey(k => k + 1)
     ↓
8. AnalyticsDashboard recibe refreshKey nuevo
     ↓
9. Todos los hooks se re-ejecutan (refreshKey cambió sus deps)
   - useResumen() → GET /resumen  ← ahora el programa INACTIVO no cuenta
   - useDistribucionProgramas() → GET /distribucion/programas
   - useModalidad() → GET /distribucion/modalidad
   - useRanking() → GET /desempeno/ranking
     ↓
10. Las tarjetas se actualizan con los nuevos conteos
```

---

## 9. Resumen Técnico

| Aspecto | Java | Python | React |
|---------|------|--------|-------|
| Framework | Spring Boot 4.0.3 | FastAPI 0.115.6 | Vite 8 + React 19 |
| Puerto | 8081 | 8000 | 5175 |
| Base de datos | PostgreSQL (JPA/Hibernate) | PostgreSQL (pandas/read_sql) | N/A (solo localStorage) |
| Memoria | Sesiones por request | BD completa en RAM | localStorage (token + usuario) |
| Archivos | ~50 .java | 9 .py + 7 .txt datos | ~20 .jsx + .css |
| Rol principal | CRUD + Auth + Email | Analytics + Reportes | UI + Routing |
| Endpoints | ~40 REST | 21 (analytics) | N/A |
| Seguridad | JWT generado pero NO validado | Sin autenticación | Token en localStorage |

---

## 10. Diagrama de Directorios

### Frontend (React)
```
Practica/src/
├── main.jsx
├── App.jsx
├── index.css
├── components/
│   ├── charts/
│   │   ├── StatCard.jsx
│   │   ├── PieChartCard.jsx
│   │   ├── BarChartCard.jsx
│   │   └── ChartSkeleton.jsx
│   ├── footer.jsx
│   └── navbar.jsx
├── context/ThemeContext.jsx
├── hooks/useAnalytics.js
├── layouts/
│   ├── MainLayout.jsx
│   └── AuthLayout.jsx
├── pages/
│   ├── LandingPage.jsx
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── AdmonMain.jsx
│   ├── AnalyticsDashboard.jsx
│   ├── RecuperarContrasena.jsx
│   ├── dashboard/
│   │   ├── EstudianteDashboard.jsx
│   │   └── ProfesorDashboard.jsx
│   └── completar/
│       ├── FormEstudiante.jsx
│       ├── FormProfesor.jsx
│       └── FormAdministrador.jsx
├── router/AppRouter.jsx
└── services/
    ├── api.js
    └── analyticsService.js
```

### Backend Java
```
sistemadenotas/src/main/java/com/example/sistemadenotas/
├── SistemadenotasApplication.java
├── config/
│   ├── CorsConfig.java
│   ├── SecurityConfig.java
│   └── GlobalExceptionHandler.java
├── controller/      (11 controllers)
├── service/         (12 services)
├── repository/      (10 repositories)
├── model/
│   ├── dto/UsuarioDTO.java
│   ├── embeddable/NombreCompleto.java
│   ├── entity/      (10 entities)
│   └── enums/       (4 enums)
└── resources/
    └── application.properties
```

### Backend Python
```
sistema-notas/
├── main_api.py      # Servidor FastAPI
├── main.py          # CLI offline
├── database.py      # Conexión PostgreSQL
├── carga.py         # Carga de datos
├── analisis.py      # Funciones de análisis
├── limpieza.py      # Validación calidad
├── reportes.py      # Generación reportes
├── grafico.py       # Gráficos (no usado)
├── seed_data.py     # Datos sintéticos
├── data/
│   ├── raw/         # Datos mock (7 archivos)
│   └── processed/   # Reportes generados
└── .env             # Credenciales BD
```

---

*Documento generado el 15 de Mayo de 2026*
