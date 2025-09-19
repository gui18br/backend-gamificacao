from pydantic import BaseModel
from typing import Optional

class AlunoBase(BaseModel):
    matricula: Optional[str] = None
    nickname: Optional[str] = None
    
class AlunoCreate(AlunoBase):
    pass

class AlunoRegister(BaseModel):
    matricula: str
    nickname: str

class AlunoResponse(AlunoBase):
    id: int
    user_id: int
    
    
    class Config:
        orm_mode = True