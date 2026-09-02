from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Categoria, Producto

async def listar_productos(db: AsyncSession, categoria: str | None = None, estado: str | None = None, ordenar: str = 'recientes') -> list[Producto]:
    query = select(Producto).join(Producto.categoria).options(selectinload(Producto.categoria)).where(Producto.activo.is_(True))
    if categoria:
        query = query.where(Categoria.slug == categoria)
    if estado:
        query = query.where(Producto.estado == estado)
    if ordenar == 'precio_asc':
        query = query.order_by(Producto.precio.asc())
    elif ordenar == 'precio_desc':
        query = query.order_by(Producto.precio.desc())
    elif ordenar == 'rentabilidad_desc':
        query = query.order_by(Producto.rentabilidad_estimada.desc())
    else:
        query = query.order_by(Producto.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def listar_categorias(db: AsyncSession) -> list[Categoria]:
    result = await db.execute(select(Categoria).order_by(Categoria.nombre))
    return list(result.scalars().all())


async def obtener_producto(db: AsyncSession, product_id: UUID) -> Producto | None:
    return await db.scalar(select(Producto).options(selectinload(Producto.categoria)).where(Producto.id == product_id, Producto.activo.is_(True)))
