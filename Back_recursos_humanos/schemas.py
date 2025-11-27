# Schemas de Pydantic
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from decimal import Decimal

class EmpleadoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    documento: str = Field(..., min_length=1, max_length=20)
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    area: Optional[str] = Field(None, max_length=50)
    sueldo: Optional[Decimal] = Field(None, ge=0)
    fecha_ingreso: Optional[date] = None

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    documento: Optional[str] = Field(None, min_length=1, max_length=20)
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    area: Optional[str] = Field(None, max_length=50)
    sueldo: Optional[Decimal] = Field(None, ge=0)
    fecha_ingreso: Optional[date] = None

class EmpleadoResponse(EmpleadoBase):
    id: int
    
    class Config:
        from_attributes = True
