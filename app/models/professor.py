from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Professor(Base):
    __tablename__ = "professores"
    
    matricula = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=True)
    avatar_id = Column(Integer, ForeignKey("avatars.id"), nullable=True)

    avatar = relationship("Avatar", backref="professores")