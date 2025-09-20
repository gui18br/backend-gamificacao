from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Aluno(Base):
    __tablename__ = "alunos"
    
    matricula = Column(String, primary_key=True, index=True)
    nickname = Column(String, unique=True, nullable=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=True)
    icone = Column(String, nullable=True)
    
