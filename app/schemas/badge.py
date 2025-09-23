from pydantic import BaseModel

class BadgeBase(BaseModel):
    id: int
    nome: str
    requisito: str
    icone: str
    
class BadgeResponse(BadgeBase):
    id: int
    
    class Config:
        orm_mode = True