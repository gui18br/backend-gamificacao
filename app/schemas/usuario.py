from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    nome: EmailStr
    icone: str
    tipo: str
    
class UserCreate(UserBase):
    senha: str
    
class UserResponse(UserBase):
    id: int
    tipo_user: str
    access_token: str
    
    class Config:
        orm_mode = True