from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DragonTeam Logistics API")

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:3000", # React default
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to DragonTeam Logistics API"}

# --- Chofer Endpoints ---
@app.post("/choferes/", response_model=schemas.Chofer)
def create_chofer(chofer: schemas.ChoferCreate, db: Session = Depends(get_db)):
    db_chofer = crud.get_chofer_by_email(db, email=chofer.email)
    if db_chofer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_chofer(db=db, chofer=chofer)

@app.get("/choferes/", response_model=List[schemas.Chofer])
def read_choferes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    choferes = crud.get_choferes(db, skip=skip, limit=limit)
    return choferes

@app.get("/choferes/{chofer_id}", response_model=schemas.Chofer)
def read_chofer(chofer_id: int, db: Session = Depends(get_db)):
    db_chofer = crud.get_chofer(db, chofer_id=chofer_id)
    if db_chofer is None:
        raise HTTPException(status_code=404, detail="Chofer not found")
    return db_chofer

# --- Pedido Endpoints ---
@app.post("/pedidos/", response_model=schemas.Pedido)
def create_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return crud.create_pedido(db=db, pedido=pedido)

@app.get("/pedidos/", response_model=List[schemas.Pedido])
def read_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pedidos(db, skip=skip, limit=limit)

@app.put("/pedidos/{pedido_id}/assign", response_model=schemas.Pedido)
def assign_pedido_to_chofer(pedido_id: int, chofer_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.get_pedido(db, pedido_id=pedido_id)
    if not db_pedido:
         raise HTTPException(status_code=404, detail="Pedido not found")
    
    db_chofer = crud.get_chofer(db, chofer_id=chofer_id)
    if not db_chofer:
        raise HTTPException(status_code=404, detail="Chofer not found")
        
    return crud.assign_pedido(db=db, pedido_id=pedido_id, chofer_id=chofer_id)

# --- Ubicacion Endpoints (Critical) ---
@app.post("/ubicacion/", response_model=schemas.Ubicacion)
def create_ubicacion(ubicacion: schemas.UbicacionCreate, db: Session = Depends(get_db)):
    # Verify chofer exists
    db_chofer = crud.get_chofer(db, chofer_id=ubicacion.chofer_id)
    if not db_chofer:
        raise HTTPException(status_code=404, detail="Chofer not found")
        
    return crud.create_ubicacion(db=db, ubicacion=ubicacion)

@app.get("/ubicacion/{chofer_id}", response_model=List[schemas.Ubicacion])
def read_ubicaciones_chofer(chofer_id: int, db: Session = Depends(get_db)):
    return crud.get_ubicaciones_by_chofer(db, chofer_id=chofer_id)

# Agrégalo en main.py en la sección de Ubicacion
@app.get("/ubicacion/", response_model=List[schemas.Ubicacion])
def read_all_ubicaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Ubicacion).offset(skip).limit(limit).all()
