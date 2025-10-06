from pydantic import BaseModel

class AvatarBase(BaseModel):
    id: int
    caminho_foto: str
    nome: str
        
class AvatarResponse(AvatarBase):
    id: int
    
    class Config:
        from_attributes = True
