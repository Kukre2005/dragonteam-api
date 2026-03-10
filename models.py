from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base

class EstadoPedido(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    EN_CAMINO = "EN_CAMINO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

class Chofer(Base):
    __tablename__ = "choferes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pedidos = relationship("Pedido", back_populates="chofer")
    ubicaciones = relationship("Ubicacion", back_populates="chofer")

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, index=True)
    direccion_origen = Column(String)
    direccion_destino = Column(String)
    estado = Column(Enum(EstadoPedido, native_enum=False), default=EstadoPedido.PENDIENTE)
    chofer_id = Column(Integer, ForeignKey("choferes.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chofer = relationship("Chofer", back_populates="pedidos")

class Ubicacion(Base):
    __tablename__ = "ubicaciones"

    id = Column(Integer, primary_key=True, index=True)
    chofer_id = Column(Integer, ForeignKey("choferes.id"))
    latitud = Column(Float)
    longitud = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    chofer = relationship("Chofer", back_populates="ubicaciones")
