import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, func
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
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    productos: Mapped[list['Producto']] = relationship(back_populates='categoria')

class Producto(Timestamped):
    __tablename__ = 'productos'
    __table_args__ = (CheckConstraint('precio >= 0', name='ck_productos_precio_no_negativo'), CheckConstraint('rentabilidad_estimada >= 0', name='ck_productos_rentabilidad_no_negativa'), CheckConstraint('stock >= 0', name='ck_productos_stock_no_negativo'), Index('ix_productos_activo', 'activo'))
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    categoria_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('categorias.id'), index=True)
    nombre: Mapped[str] = mapped_column(String(150))
    descripcion: Mapped[str] = mapped_column(Text)
    ubicacion: Mapped[str] = mapped_column(String(180))
    sku: Mapped[str] = mapped_column(String(30), unique=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    rentabilidad_estimada: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    stock: Mapped[int] = mapped_column(Integer, default=1, server_default='1')
    imagen_url: Mapped[str] = mapped_column(String(500))
    estado: Mapped[str] = mapped_column(String(30), default='disponible', server_default='disponible')
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    categoria: Mapped[Categoria] = relationship(back_populates='productos')
