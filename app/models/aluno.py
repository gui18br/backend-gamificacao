from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Aluno(Base):
    __tablename__ = "alunos"
    
    matricula = Column(String, primary_key=True, index=True)
    nickname = Column(String, unique=True, nullable=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=True)
    xp = Column(String, nullable=True)
    nivel = Column(String, nullable=True)
    
    avatar_id = Column(Integer, ForeignKey("avatars.id"), nullable=True)

    avatar = relationship("Avatar", backref="alunos")