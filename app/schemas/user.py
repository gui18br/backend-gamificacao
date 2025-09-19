from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    
class UserCreate(UserBase):
    password: str
    
class UserResponse(UserBase):
    id: int
    tipo: str
    
    class Config:
        orm_mode = True