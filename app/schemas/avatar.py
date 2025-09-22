from pydantic import BaseModel

class AvatarBase(BaseModel):
    id: int
    caminho_foto: str
    nome: str
    
    class Config:
        orm_mode = True