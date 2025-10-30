from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import database
from app.schemas import avatar as schemas
from app.models import avatar as models
from app.models.avatar import Avatar 

router = APIRouter(prefix="/avatares", tags=["Avatares"])

#Nova rota: POST /avatares (CREATE / INSERT)
@router.post("/", status_code=201)
def create_avatar(
    avatar_data: Dict[str, Any] = Body(..., embed=True), 
    db: Session = Depends(database.get_db)
):
    
    nome = avatar_data.get("nome")
    caminho_foto = avatar_data.get("caminho_foto")
    
    if not caminho_foto:
         raise HTTPException(status_code=400, detail="O campo caminho_foto é obrigatório.")
    
    if nome:
        db_avatar = db.query(Avatar).filter(Avatar.nome == nome).first()
        if db_avatar:
            raise HTTPException(status_code=400, detail="Nome de Avatar já registrado")

    new_avatar = Avatar(
        nome=nome,
        caminho_foto=caminho_foto
    )

    db.add(new_avatar)
    db.commit()
    db.refresh(new_avatar)
    
    return {"data": new_avatar}

@router.get("/", response_model=List[schemas.AvatarBase])
def get_avatares(db: Session = Depends(database.get_db)):
    avatares = db.query(models.Avatar).all()
    return avatares

@router.get("/{id}", response_model=schemas.AvatarResponse)
def get_avatar_by_id(id: int, db: Session = Depends(database.get_db)):
    avatar = db.query(models.Avatar).filter(models.Avatar.id == id).first()
    
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar não encontrado")
    
    return avatar