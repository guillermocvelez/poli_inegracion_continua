#En este archivo vn los modelos SQL Alchemy
from database import Base
from sqlalchemy import Column, Integer, String, Numeric, Date, CheckConstraint
from datetime import date

class Empleado(Base):
    __tablename__ = "empleados"
    __table_args__ = {'schema': 'gestion_humana'}
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    documento = Column(String(20), nullable=False, unique=True)
    correo = Column(String(100))
    telefono = Column(String(20))
    area = Column(String(50))
    sueldo = Column(Numeric(12, 2), CheckConstraint('sueldo >= 0'))
    fecha_ingreso = Column(Date, default=date.today)
