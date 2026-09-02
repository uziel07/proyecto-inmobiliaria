from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Cliente, Usuario


async def listar_clientes(db: AsyncSession) -> list[Cliente]:
    result = await db.execute(select(Cliente).options(selectinload(Cliente.usuario)).order_by(Cliente.created_at.desc()))
    return list(result.scalars().all())


async def obtener_cliente(db: AsyncSession, cliente_id: UUID) -> Cliente | None:
    return await db.scalar(select(Cliente).options(selectinload(Cliente.usuario)).where(Cliente.id == cliente_id))


async def crear_cliente(db: AsyncSession, email: str, nombre: str, documento: str, telefono: str | None) -> Cliente:
    usuario = Usuario(email=email, nombre=nombre)
    db.add(usuario)
    await db.flush()
    cliente = Cliente(usuario_id=usuario.id, documento=documento, telefono=telefono)
    db.add(cliente)
    await db.commit()
    await db.refresh(cliente)
    await db.refresh(cliente, ['usuario'])
    return cliente


async def actualizar_cliente(db: AsyncSession, cliente: Cliente, email: str | None = None, nombre: str | None = None, documento: str | None = None, telefono: str | None = None, activo: bool | None = None) -> Cliente:
    if cliente.usuario_id is not None:
        usuario = await db.get(Usuario, cliente.usuario_id)
        if usuario:
            if email is not None:
                usuario.email = email
            if nombre is not None:
                usuario.nombre = nombre
            if activo is not None:
                usuario.activo = activo
    if documento is not None:
        cliente.documento = documento
    if telefono is not None:
        cliente.telefono = telefono
    await db.commit()
    await db.refresh(cliente)
    await db.refresh(cliente, ['usuario'])
    return cliente


async def eliminar_cliente(db: AsyncSession, cliente: Cliente) -> None:
    await db.delete(cliente)
    if cliente.usuario_id is not None:
        usuario = await db.get(Usuario, cliente.usuario_id)
        if usuario:
            await db.delete(usuario)
    await db.commit()
