from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Producto

async def listar_productos(db: AsyncSession) -> list[Producto]:
    result = await db.execute(select(Producto).options(selectinload(Producto.categoria)).where(Producto.activo.is_(True)).order_by(Producto.created_at.desc()))
    return list(result.scalars().all())
