from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.productos import categorias_router, router as productos_router
from app.api.routes.clientes import router as clientes_router
from app.core.config import settings

app = FastAPI(title='Nido Capital API', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=[settings.cors_origins], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(productos_router)
app.include_router(categorias_router)
app.include_router(clientes_router)

@app.get('/health', tags=['Sistema'])
async def health() -> dict[str, str]: return {'status':'ok', 'service':'nido-capital'}
