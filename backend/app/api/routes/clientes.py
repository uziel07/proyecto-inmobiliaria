from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.db.session import get_db
from app.models import Cliente, Usuario
from app.schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services.cliente_service import actualizar_cliente, crear_cliente, eliminar_cliente, listar_clientes, obtener_cliente

router = APIRouter(prefix='/clientes', tags=['Clientes'])


@router.get('', response_model=list[ClienteResponse])
async def obtener_clientes(db: AsyncSession = Depends(get_db)) -> list[Cliente]:
    return await listar_clientes(db)


@router.get('/{cliente_id}', response_model=ClienteResponse)
async def obtener_cliente_por_id(cliente_id: UUID, db: AsyncSession = Depends(get_db)) -> Cliente:
    cliente = await obtener_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')
    return cliente


@router.post('', response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente_nuevo(payload: ClienteCreate, db: AsyncSession = Depends(get_db)) -> Cliente:
    if await db.scalar(select(Usuario).where(Usuario.email == payload.email)) is not None:
        raise HTTPException(status_code=409, detail='El email ya está registrado')
    if await db.scalar(select(Cliente).where(Cliente.documento == payload.documento)) is not None:
        raise HTTPException(status_code=409, detail='El documento ya está registrado')
    try:
        return await crear_cliente(db, payload.email, payload.nombre, payload.documento, payload.telefono)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail='No se pudo guardar el cliente') from None


@router.put('/{cliente_id}', response_model=ClienteResponse)
async def actualizar_cliente_existente(cliente_id: UUID, payload: ClienteUpdate, db: AsyncSession = Depends(get_db)) -> Cliente:
    cliente = await obtener_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')
    if payload.email is not None and await db.scalar(select(Usuario).where(Usuario.email == payload.email, Usuario.id != cliente.usuario_id)) is not None:
        raise HTTPException(status_code=409, detail='El email ya está registrado')
    if payload.documento is not None and await db.scalar(select(Cliente).where(Cliente.documento == payload.documento, Cliente.id != cliente_id)) is not None:
        raise HTTPException(status_code=409, detail='El documento ya está registrado')
    try:
        return await actualizar_cliente(db, cliente, payload.email, payload.nombre, payload.documento, payload.telefono, payload.activo)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail='No se pudo actualizar el cliente') from None


@router.delete('/{cliente_id}', status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_cliente_existente(cliente_id: UUID, db: AsyncSession = Depends(get_db)) -> None:
    cliente = await obtener_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')
    await eliminar_cliente(db, cliente)
