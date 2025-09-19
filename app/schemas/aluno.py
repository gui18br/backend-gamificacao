from pydantic import BaseModel

class AlunoBase(BaseModel):
    matricula: str
    
class AlunoCreate(AlunoBase):
    pass

class AlunoResponse(AlunoBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True