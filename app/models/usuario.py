from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullalble=True)
    icone = Column(String, nullable=True)
    tipo = Column(String, nullable=False)
    
    aluno = relationship("Aluno", back_populates="usuario", uselist=False)
    professor = relationship("Professor", back_populates="usuario", uselist=False)
    
    