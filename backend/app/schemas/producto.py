from decimal import Decimal
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class CategoriaResponse(BaseModel):
    id: UUID
    nombre: str
    slug: str
    model_config = ConfigDict(from_attributes=True)

class ProductoResponse(BaseModel):
    id: UUID
    nombre: str
    descripcion: str
    ubicacion: str
    sku: str
    precio: Decimal
    rentabilidad_estimada: Decimal
    stock: int
    imagen_url: str
    estado: str
    activo: bool
    categoria: CategoriaResponse
    model_config = ConfigDict(from_attributes=True)


class ProductoCreate(BaseModel):
    categoria_id: UUID
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: str = Field(min_length=10)
    ubicacion: str = Field(min_length=2, max_length=180)
    sku: str = Field(min_length=2, max_length=30)
    precio: Decimal = Field(ge=0, max_digits=14, decimal_places=2)
    rentabilidad_estimada: Decimal = Field(ge=0, le=100, max_digits=5, decimal_places=2)
    stock: int = Field(default=1, ge=0)
    imagen_url: str = Field(default='/images/properties/property-placeholder.svg', max_length=500)
    estado: Literal['disponible', 'en_oferta', 'alquilada', 'reservada'] = 'disponible'
    activo: bool = True
