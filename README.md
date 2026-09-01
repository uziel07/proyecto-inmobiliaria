# Nido Capital

Aplicación básica de clase para explorar oportunidades de inversión inmobiliaria. El frontend usa Angular 21 y el backend FastAPI entrega propiedades almacenadas en PostgreSQL. Las tablas técnicas incluyen usuarios, clientes, productos, categorías, carritos, detalles de carrito, pedidos y detalles de pedido.

## Ejecución

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec backend alembic upgrade head
curl http://localhost:8000/health
curl http://localhost:8000/productos
cd frontend
npm install
npm start
```

En este repositorio el frontend está en la raíz, por lo que el último bloque puede ejecutarse como `npm install` y `npm start` desde la carpeta del proyecto.

- Frontend: http://localhost:4200
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## DBeaver

Crear una conexión PostgreSQL con host `localhost`, puerto `5432`, base de datos igual a `POSTGRES_DB`, usuario igual a `POSTGRES_USER` y contraseña igual a `POSTGRES_PASSWORD` del archivo `.env`.

## Estructura

- `src/app/components`: interfaz standalone, señales y componentes visuales.
- `src/app/services`: consumo tipado de la API.
- `backend/app`: configuración, modelos SQLAlchemy, esquemas Pydantic, servicios y rutas.
- `backend/alembic`: migración inicial con registros inmobiliarios demo.
