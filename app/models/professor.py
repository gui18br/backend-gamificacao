from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Professor(Base):
    __tablename__ = "professores"
    
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    
    usuario = relationship("Usuario", back_populates="professor")