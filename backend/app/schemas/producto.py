from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class CategoriaResponse(BaseModel):
    id: UUID
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class ProductoResponse(BaseModel):
    id: UUID
    nombre: str
    descripcion: str
    ubicacion: str
    sku: str
    precio: Decimal
    rentabilidad_estimada: Decimal
    imagen_url: str
    estado: str
    activo: bool
    categoria: CategoriaResponse
    model_config = ConfigDict(from_attributes=True)
