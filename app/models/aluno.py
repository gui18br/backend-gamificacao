from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Aluno(Base):
    __tablename__ = "alunos"
    
    id = Column(Integer, ForeignKey("Usuarios.id"), primary_key=True)
    matricula = Column(String, unique=True, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    
    usuario = relationship("Usuario", back_populates="aluno")