from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Atividade(Base):
    __tablename__ = "Turma"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    
    professor_id_fk = Column(Integer, ForeignKey("Professor.id"), nullable=True)

    professor = relationship("Professor", backref="Turma")
