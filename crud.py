from sqlalchemy.orm import Session
import models, schemas

# --- Chofer CRUD ---
def get_chofer(db: Session, chofer_id: int):
    return db.query(models.Chofer).filter(models.Chofer.id == chofer_id).first()

def get_chofer_by_email(db: Session, email: str):
    return db.query(models.Chofer).filter(models.Chofer.email == email).first()

def get_choferes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chofer).offset(skip).limit(limit).all()

def create_chofer(db: Session, chofer: schemas.ChoferCreate):
    db_chofer = models.Chofer(
        nombre=chofer.nombre, 
        email=chofer.email, 
        activo=chofer.activo
    )
    db.add(db_chofer)
    db.commit()
    db.refresh(db_chofer)
    return db_chofer

# --- Pedido CRUD ---
def create_pedido(db: Session, pedido: schemas.PedidoCreate):
    db_pedido = models.Pedido(**pedido.model_dump())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def get_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pedido).offset(skip).limit(limit).all()

def get_pedido(db: Session, pedido_id: int):
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

def assign_pedido(db: Session, pedido_id: int, chofer_id: int):
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if db_pedido:
        db_pedido.chofer_id = chofer_id
        db_pedido.estado = models.EstadoPedido.EN_CAMINO # Assuming assignment implies en camino for MVP
        db.commit()
        db.refresh(db_pedido)
    return db_pedido

# --- Ubicacion CRUD ---
def create_ubicacion(db: Session, ubicacion: schemas.UbicacionCreate):
    db_ubicacion = models.Ubicacion(**ubicacion.model_dump())
    db.add(db_ubicacion)
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion

def get_ubicaciones_by_chofer(db: Session, chofer_id: int, limit: int = 10):
    return db.query(models.Ubicacion).filter(models.Ubicacion.chofer_id == chofer_id).order_by(models.Ubicacion.timestamp.desc()).limit(limit).all()
