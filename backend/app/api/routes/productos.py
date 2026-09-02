from typing import Literal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.db.session import get_db
from app.models import Categoria, Producto
from app.schemas.producto import CategoriaResponse, ProductoCreate, ProductoResponse
from app.services.producto_service import listar_categorias, listar_productos, obtener_producto

router = APIRouter(prefix='/productos', tags=['Productos'])
categorias_router = APIRouter(prefix='/categorias', tags=['Categorías'])

@categorias_router.get('', response_model=list[CategoriaResponse])
async def obtener_categorias(db: AsyncSession = Depends(get_db)) -> list[Categoria]:
    return await listar_categorias(db)


@router.get('', response_model=list[ProductoResponse])
async def obtener_productos(
    categoria: str | None = None,
    estado: Literal['disponible', 'en_oferta', 'alquilada', 'reservada'] | None = None,
    ordenar: Literal['recientes', 'precio_asc', 'precio_desc', 'rentabilidad_desc'] = Query('recientes'),
    db: AsyncSession = Depends(get_db),
) -> list[Producto]:
    return await listar_productos(db, categoria, estado, ordenar)


@router.get('/{product_id}', response_model=ProductoResponse)
async def obtener_producto_por_id(product_id: UUID, db: AsyncSession = Depends(get_db)) -> Producto:
    product = await obtener_producto(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail='Propiedad no encontrada')
    return product


@router.post('', response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(payload: ProductoCreate, db: AsyncSession = Depends(get_db)) -> Producto:
    if await db.scalar(select(Categoria).where(Categoria.id == payload.categoria_id)) is None:
        raise HTTPException(status_code=404, detail='La categoría no existe')
    if await db.scalar(select(Producto).where(Producto.sku == payload.sku)) is not None:
        raise HTTPException(status_code=409, detail='El SKU ya está registrado')
    product = Producto(**payload.model_dump())
    db.add(product)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail='No se pudo guardar la propiedad') from None
    await db.refresh(product)
    await db.refresh(product, ['categoria'])
    return product
