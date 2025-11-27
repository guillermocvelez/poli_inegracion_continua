#En este archivo vn los modelos SQL Alchemy
from database import Base
from sqlalchemy import Column, Integer, String, Numeric, Date, CheckConstraint
from datetime import date
import os

class Empleado(Base):
    __tablename__ = "empleados"
    # Solo usar schema en producción (PostgreSQL), no en tests (SQLite)
    __table_args__ = {'schema': 'gestion_humana'} if not os.getenv("TESTING") else {}
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    documento = Column(String(20), nullable=False, unique=True)
    correo = Column(String(100))
    telefono = Column(String(20))
    area = Column(String(50))
    sueldo = Column(Numeric(12, 2), CheckConstraint('sueldo >= 0'))
    fecha_ingreso = Column(Date, default=date.today)
