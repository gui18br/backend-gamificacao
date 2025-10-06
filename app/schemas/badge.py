from typing import List
from pydantic import BaseModel

class BadgeBase(BaseModel):
    id: int
    nome: str
    requisito: str
    icone: str
    
class BadgeResponse(BadgeBase):
    id: int
    nome: str
    requisito: str
    icone: str
    
class BadgeResponseList(BaseModel):
    data: List[BadgeResponse]
        
    class Config:
        from_attributes = True
        
class BadgeResponseSingle(BaseModel):
    data: BadgeResponse     
     
    class Config:
        from_attributes = True