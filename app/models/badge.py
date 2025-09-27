from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .database import Base
from .aluno_badge import aluno_badge

class Badge(Base):
    __tablename__ = "Badge"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    requisito = Column(String, nullable=True)
    icone = Column(String, nullable=True)
    
    alunos_associados = relationship("AlunoBadge", back_populates="badge")
