# Nido Capital

Aplicación básica de clase para explorar oportunidades de inversión inmobiliaria. El frontend usa Angular 21 y el backend FastAPI entrega propiedades almacenadas en PostgreSQL. El esquema mínimo usa usuarios, clientes, productos y categorías.

## Ejecución

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.scripts.seed
curl http://localhost:8000/health
curl http://localhost:8000/productos
npm install
npm start
```

En este repositorio el frontend está en la raíz, por lo que el último bloque puede ejecutarse como `npm install` y `npm start` desde la carpeta del proyecto.

Para ejecutar el backend directamente sin Docker, entra en `backend` y usa:

```bash
python -m uvicorn app.main:app --reload
```

- Frontend: http://localhost:4200
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

La API consulta PostgreSQL en cada solicitud. El catálogo se actualiza automáticamente cada 5 segundos en desarrollo y también puede actualizarse con el botón “Actualizar propiedades”.

Endpoints principales:

- `GET /categorias`
- `GET /productos?categoria=casas-de-lujo&estado=disponible`
- `GET /productos/{id}`
- `POST /productos`

El script `backend/app/scripts/seed.py` es idempotente y carga diez propiedades. Para probar una inserción desde DBeaver, ejecutar `database/test_insert.sql` y esperar el sondeo o pulsar el botón de actualización.

## DBeaver

Crear una conexión PostgreSQL con host `localhost`, puerto `5432`, base de datos igual a `POSTGRES_DB`, usuario igual a `POSTGRES_USER` y contraseña igual a `POSTGRES_PASSWORD` del archivo `.env`.

## Estructura

- `src/app/components`: interfaz standalone, señales y componentes visuales.
- `src/app/services`: consumo tipado de la API.
- `backend/app`: configuración, modelos SQLAlchemy, esquemas Pydantic, servicios y rutas.
- `backend/alembic`: migración inicial con registros inmobiliarios demo.
