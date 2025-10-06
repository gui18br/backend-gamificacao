from pydantic import BaseModel
from typing import List, Optional

class AlunoBase(BaseModel):
    matricula: str
    nome: str
    nickname: str
    senha: str
    xp: str
    nivel: str
    icone: str | None = None
    avatar_id_fk: int
    
class AlunoCreate(AlunoBase):
    pass

class AlunoResponseList(BaseModel):
    data: List[AlunoBase]
        
    class Config:
        from_attributes = True
        
class AlunoResponseSingle(BaseModel):
    data: AlunoBase
    
    class Config:
        from_attributes = True        

class AlunoResponseCreate(BaseModel):
    data: dict
  
