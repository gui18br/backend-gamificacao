from pydantic import BaseModel

class ProfessorBase(BaseModel):
    pass
    
class ProfessorCreate(ProfessorBase):
    pass

class ProfessorResponse(ProfessorBase):
    id: int
    
    class Config:
        orm_mod = True