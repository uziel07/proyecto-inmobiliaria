import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Timestamped(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Usuario(Timestamped):
    __tablename__ = 'usuarios'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class Cliente(Timestamped):
    __tablename__ = 'clientes'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('usuarios.id'), unique=True)
    documento: Mapped[str] = mapped_column(String(30), unique=True)
    telefono: Mapped[str | None] = mapped_column(String(30))
    usuario: Mapped[Usuario] = relationship()

class Categoria(Timestamped):
    __tablename__ = 'categorias'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(80), unique=True)
    productos: Mapped[list['Producto']] = relationship(back_populates='categoria')

class Producto(Timestamped):
    __tablename__ = 'productos'
    __table_args__ = (CheckConstraint('precio >= 0', name='ck_productos_precio_no_negativo'), CheckConstraint('rentabilidad_estimada >= 0', name='ck_productos_rentabilidad_no_negativa'), Index('ix_productos_activo', 'activo'))
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    categoria_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('categorias.id'), index=True)
    nombre: Mapped[str] = mapped_column(String(150))
    descripcion: Mapped[str] = mapped_column(Text)
    ubicacion: Mapped[str] = mapped_column(String(180))
    sku: Mapped[str] = mapped_column(String(30), unique=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    rentabilidad_estimada: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    imagen_url: Mapped[str] = mapped_column(String(500))
    estado: Mapped[str] = mapped_column(String(30), default='Disponible')
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    categoria: Mapped[Categoria] = relationship(back_populates='productos')

class Carrito(Timestamped):
    __tablename__ = 'carritos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('usuarios.id'))

class DetalleCarrito(Timestamped):
    __tablename__ = 'detalles_carrito'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    carrito_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('carritos.id'))
    producto_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('productos.id'))
    cantidad: Mapped[int] = mapped_column(default=1)

class Pedido(Timestamped):
    __tablename__ = 'pedidos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('clientes.id'))
    estado: Mapped[str] = mapped_column(String(30), default='Pendiente')
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)

class DetallePedido(Timestamped):
    __tablename__ = 'detalles_pedido'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pedido_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('pedidos.id'))
    producto_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('productos.id'))
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    cantidad: Mapped[int] = mapped_column(default=1)
