from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Atividade(Base):
    __tablename__ = "Atividade"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    nota_max = Column(String, nullable=True)
    pontos = Column(String, nullable=True)
    data_entrega = Column(Date, nullable=False),
    
    badge_id_fk = Column(Integer, ForeignKey("Badge.id"), nullable=True)
    turma_id_fk = Column(Integer, ForeignKey("Turma.id"), nullable=True)

    badge = relationship("Badge", backref="Atividade")
    turma = relationship("Turma", backref="Atividade")