from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Atividade(Base):
    __tablename__ = "atividades"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    nota_max = Column(String, nullable=True)
    pontos = Column(String, nullable=True)
    
    badge_id_fk = Column(Integer, ForeignKey("badge.id"), nullable=True)
    turma_id_fk = Column(Integer, ForeignKey("turma.id"), nullable=True)

    badge = relationship("Badge", backref="atividades")
    turma = relationship("Turma", backref="atividades")