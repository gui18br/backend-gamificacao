from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.schemas import avatar as schemas
from app.models import avatar as models

router  = APIRouter(prefix="/avatares", tags=["Avatares"])

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