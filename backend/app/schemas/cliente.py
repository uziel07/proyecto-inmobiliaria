from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class UsuarioResponse(BaseModel):
    id: UUID
    email: str
    nombre: str
    activo: bool
    model_config = ConfigDict(from_attributes=True)


class ClienteResponse(BaseModel):
    id: UUID
    usuario_id: Optional[UUID]
    documento: str
    telefono: Optional[str]
    usuario: Optional[UsuarioResponse] = None
    model_config = ConfigDict(from_attributes=True)


class ClienteCreate(BaseModel):
    email: str = Field(min_length=3, max_length=180)
    nombre: str = Field(min_length=2, max_length=120)
    documento: str = Field(min_length=3, max_length=30)
    telefono: Optional[str] = Field(default=None, max_length=30)


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=120)
    email: Optional[str] = Field(default=None, min_length=3, max_length=180)
    documento: Optional[str] = Field(default=None, min_length=3, max_length=30)
    telefono: Optional[str] = Field(default=None, max_length=30)
    activo: Optional[bool] = None
