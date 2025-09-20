from pydantic import BaseModel

class ProfessorBase(BaseModel):
    nome: str
    email: str
    senha: str
    icone: str | None = None
    
class ProfessorCreate(ProfessorBase):
    pass

class ProfessorResponse(ProfessorBase):
    id: int
    
    class Config:
        orm_mod = True