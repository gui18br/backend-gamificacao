from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router  = APIRouter(prefix="/avatares", tags=["Avatares"])

@router.get("/", response_model=List[schemas.AvatarBase])
def get_avatares(db: Session = Depends(database.get_db)):
    avatares = db.query(models.Avatar).all()
    return avatares