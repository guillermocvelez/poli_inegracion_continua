from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import models, schemas
from database import SessionLocal, engine

app = FastAPI(title="HR API", description="API de Gestión de Recursos Humanos", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas
models.Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "HR API del Politecnico Grancolombiano - CRUD de Empleados"}

# CREATE - Crear un nuevo empleado
@app.post("/empleados", response_model=schemas.EmpleadoResponse, status_code=status.HTTP_201_CREATED)
def create_empleado(empleado: schemas.EmpleadoCreate, db: Session = Depends(get_db)):
    try:
        db_empleado = models.Empleado(**empleado.model_dump())
        db.add(db_empleado)
        db.commit()
        db.refresh(db_empleado)
        return db_empleado
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El documento {empleado.documento} ya está registrado"
        )

# READ - Obtener todos los empleados
@app.get("/empleados", response_model=List[schemas.EmpleadoResponse])
def get_empleados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    empleados = db.query(models.Empleado).offset(skip).limit(limit).all()
    return empleados

# READ - Obtener un empleado por ID
@app.get("/empleados/{empleado_id}", response_model=schemas.EmpleadoResponse)
def get_empleado(empleado_id: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con ID {empleado_id} no encontrado"
        )
    return empleado

# UPDATE - Actualizar un empleado
@app.put("/empleados/{empleado_id}", response_model=schemas.EmpleadoResponse)
def update_empleado(empleado_id: int, empleado_update: schemas.EmpleadoUpdate, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con ID {empleado_id} no encontrado"
        )
    
    try:
        update_data = empleado_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(empleado, key, value)
        
        db.commit()
        db.refresh(empleado)
        return empleado
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El documento ya está registrado por otro empleado"
        )

# DELETE - Eliminar un empleado
@app.delete("/empleados/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_empleado(empleado_id: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con ID {empleado_id} no encontrado"
        )
    
    db.delete(empleado)
    db.commit()
    return None

# Buscar empleados por documento
@app.get("/empleados/buscar/documento/{documento}", response_model=schemas.EmpleadoResponse)
def search_by_documento(documento: str, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.documento == documento).first()
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con documento {documento} no encontrado"
        )
    return empleado
