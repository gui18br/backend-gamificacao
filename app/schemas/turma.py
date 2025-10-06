from pydantic import BaseModel
from typing import Optional

class TurmaBase(BaseModel):
    nome: str
    requisito: str
    professor_matricula_fk: int
    
class TurmaCreate(TurmaBase):
    pass

class TurmaResponse(TurmaBase):
    id: int
        
    class Config:
        from_attributes = True