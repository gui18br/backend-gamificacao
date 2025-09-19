from pydantic import BaseModel
from typing import Optional

class AlunoBase(BaseModel):
    matricula: Optional[str] = None
    nickname: Optional[str] = None
    
class AlunoCreate(AlunoBase):
    pass

class AlunoResponse(AlunoBase):
    id: int
    
    class Config:
        orm_mode = True