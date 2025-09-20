from pydantic import BaseModel
from typing import Optional

class AlunoBase(BaseModel):
    matricula: str
    nome: str
    nickname: str
    senha: str
    icone: str | None = None
    
class AlunoCreate(AlunoBase):
    pass

class AlunoResponse(AlunoBase):
    matricula: str
        
    class Config:
        orm_mode = True