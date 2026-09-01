from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.producto import ProductoResponse
from app.services.producto_service import listar_productos

router = APIRouter(prefix='/productos', tags=['Productos'])

@router.get('', response_model=list[ProductoResponse])
async def obtener_productos(db: AsyncSession = Depends(get_db)) -> list[ProductoResponse]:
    return await listar_productos(db)  # type: ignore[return-value]
