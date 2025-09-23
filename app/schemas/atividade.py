from pydantic import BaseModel
from typing import Optional

class AtividadeBase(BaseModel):
    nome: str
    nota_max: str
    pontos: str
    badge_id_fk: int
    turma_id_fk: int
    
class AtividadeCreate(AtividadeBase):
    pass

class AtividadeResponse(AtividadeBase):
    id: int
        
    class Config:
        orm_mode = True