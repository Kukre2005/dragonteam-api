from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class EstadoPedido(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_CAMINO = "EN_CAMINO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

# --- Chofer Schemas ---
class ChoferBase(BaseModel):
    nombre: str
    email: str
    activo: Optional[bool] = True

class ChoferCreate(ChoferBase):
    pass

class Chofer(ChoferBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # updated for Pydantic v2 (orm_mode in v1)

# --- Ubicacion Schemas ---
class UbicacionBase(BaseModel):
    latitud: float
    longitud: float

class UbicacionCreate(UbicacionBase):
    chofer_id: int

class Ubicacion(UbicacionBase):
    id: int
    chofer_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Pedido Schemas ---
class PedidoBase(BaseModel):
    cliente: str
    direccion_origen: str
    direccion_destino: str

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(BaseModel):
    chofer_id: Optional[int] = None
    estado: Optional[EstadoPedido] = None

class Pedido(PedidoBase):
    id: int
    estado: EstadoPedido
    chofer_id: Optional[int] = None
    created_at: datetime
    
    # Optional: Include chofer details if needed, but keeping it simple for now
    
    class Config:
        from_attributes = True
