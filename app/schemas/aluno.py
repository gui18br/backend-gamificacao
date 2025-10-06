from pydantic import BaseModel
from typing import List, Optional

class AlunoBase(BaseModel):
    matricula: str
    nome: str
    nickname: str
    senha: str
    icone: str | None = None
    
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
