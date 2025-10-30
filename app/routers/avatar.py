from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import database
from app.schemas import avatar as schemas 
from app.models.avatar import Avatar     
from typing import List

router = APIRouter(prefix="/avatares", tags=["Avatares"])

@router.post("/", response_model=schemas.AvatarResponseSingle)
def create_avatar(
    avatar: schemas.AvatarCreate,  
    db: Session = Depends(database.get_db)
):
    
    if avatar.nome:
        db_avatar = db.query(Avatar).filter(Avatar.nome == avatar.nome).first()
        if db_avatar:
            raise HTTPException(status_code=400, detail="Nome de Avatar já registrado")

    new_avatar = Avatar(
        nome=avatar.nome,
        caminho_foto=avatar.caminho_foto
    )

    db.add(new_avatar)
    db.commit()
    db.refresh(new_avatar)
    
    return {"data": new_avatar}
# -------------------------------------------------------------------

@router.get("/", response_model=schemas.AvatarResponseList)
def get_avatares(db: Session = Depends(database.get_db)):
    avatares = db.query(Avatar).all()
    return {"data": avatares}

@router.get("/{id}", response_model=schemas.AvatarResponseSingle)
def get_avatar_by_id(id: int, db: Session = Depends(database.get_db)):
    avatar = db.query(Avatar).filter(Avatar.id == id).first()
    
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar não encontrado")
    
    return {"data": avatar}
