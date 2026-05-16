# Guía de Despliegue en Render

Este documento explica cómo desplegar los 3 servicios del proyecto en Render.

---

## 1. Requisitos Previos

- Cuenta en [Render](https://render.com)
- Los archivos de configuración ya están creados:
  - `sistema-notas/Procfile` ← Python
  - `proyectoIntegrador_Backend/sistemadenotas/Dockerfile` ← Java
  - `ProyectoIntegradorFrontend/Practica/.env.production` ← React

---

## 2. Desplegar Java (Spring Boot) — Web Service

### Crear el servicio
1. Render Dashboard → **New +** → **Web Service**
2. Conecta tu repositorio (o sube el proyecto manualmente)
3. Configura:
   - **Name:** `sistema-notas-java`
   - **Runtime:** `Docker`
   - **Branch:** `main` (o la que uses)
   - **Root Directory:** `proyectoIntegrador_Backend/sistemadenotas`

### Variables de entorno
Agrega en Render Dashboard → Environment:

| Variable | Valor |
|----------|-------|
| `DB_URL` | `jdbc:postgresql://db.prisma.io:5432/postgres?sslmode=require` |
| `DB_USERNAME` | *(la misma de desarrollo)* |
| `DB_PASSWORD` | *(la misma de desarrollo)* |
| `APP_JWT_SECRET` | `clave-super-secreta-sistema-de-notas-2026-debe-ser-larga` |
| `APP_JWT_EXPIRATION` | `86400000` |
| `APP_FRONTEND_URL` | `https://sistema-notas-frontend.onrender.com` |
| `SPRING_MAIL_USERNAME` | `deimer.yav@gmail.com` |
| `SPRING_MAIL_PASSWORD` | `ssad kuhd zjud nnrn` |

Render asigna automáticamente la variable `PORT`.

### Health check
Render usará: `/api/analytics/health` (una vez que confirmes la URL).

---

## 3. Desplegar Python (FastAPI) — Web Service

### Crear el servicio
1. Render Dashboard → **New +** → **Web Service**
2. Configura:
   - **Name:** `sistema-notas-python`
   - **Runtime:** `Python 3`
   - **Root Directory:** `sistema-notas`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main_api:app --host 0.0.0.0 --port $PORT`

### Variables de entorno

| Variable | Valor |
|----------|-------|
| `DB_URL` | `jdbc:postgresql://db.prisma.io:5432/postgres?sslmode=require` |
| `DB_USERNAME` | *(la misma de desarrollo)* |
| `DB_PASSWORD` | *(la misma de desarrollo)* |
| `CORS_ORIGINS` | `https://sistema-notas-frontend.onrender.com,http://localhost:5173,http://localhost:5174,http://localhost:5175` |

### Nota importante
El Python backend carga datos en memoria al iniciar. Si se agregan datos nuevos desde Java, el Python backend no los verá hasta que alguien llame:
```
POST /api/analytics/recargar
```
Puedes llamarlo manualmente desde el navegador, o el frontend lo llama automáticamente al activar/desactivar programas.

---

## 4. Desplegar React (Frontend) — Static Site

### Crear el sitio estático
1. Render Dashboard → **New +** → **Static Site**
2. Configura:
   - **Name:** `sistema-notas-frontend`
   - **Root Directory:** `ProyectoIntegradorFrontend/Practica`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`

### Variables de entorno

| Variable | Valor |
|----------|-------|
| `VITE_API_URL` | `https://sistema-notas-python.onrender.com` |

### Paso extra: Reemplazar URLs de Java
Las llamadas a Java están hardcodeadas como `http://localhost:8081`. Después del primer deploy:
1. Render te dará la URL del servicio Java, ej: `https://sistema-notas-java.onrender.com`
2. En tu código local, busca y reemplaza **en toda la carpeta `src/`**:
   - **Buscar:** `http://localhost:8081`
   - **Reemplazar:** `https://sistema-notas-java.onrender.com`
3. Haz commit del cambio y Render lo redeployea automáticamente.

---

## 5. Diagrama de Conexión en Producción

```
┌─────────────────────────────────────┐
│  https://sistema-notas-frontend     │
│       .onrender.com (React)         │
└────────┬────────────────┬───────────┘
         │                │
         │ fetch()        │ Axios
         │                │
┌────────▼────────┐ ┌────▼──────────────┐
│ sistema-notas-  │ │ sistema-notas-    │
│ java.onrender   │ │ python.onrender   │
│ .com (Java)     │ │ .com (Python)     │
│        │        │ │                   │
└────────┼────────┘ └───────────────────┘
         │
         │ JDBC
         │
┌────────▼─────────────────────────┐
│  PostgreSQL (db.prisma.io:5432)  │
└──────────────────────────────────┘
```

---

## 6. URLs Finales (ejemplo)

| Servicio | URL |
|----------|-----|
| Frontend | `https://sistema-notas-frontend.onrender.com` |
| Java API | `https://sistema-notas-java.onrender.com` |
| Python API | `https://sistema-notas-python.onrender.com` |

---

## 7. Verificar Despliegue

Después de desplegar los 3 servicios:

1. **Java**: `https://sistema-notas-java.onrender.com/api/auth/login` → debe responder (POST)
2. **Python**: `https://sistema-notas-python.onrender.com/api/analytics/health` → debe responder `{ "status": "ok", ... }`
3. **Frontend**: Abrir la URL del frontend, hacer login y probar funcionalidades
