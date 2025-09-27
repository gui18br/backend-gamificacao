from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.models.aluno_badge import AlunoBadge

router  = APIRouter(prefix="/badges", tags=["Badges"])

@router.get("/", response_model=List[schemas.BadgeBase])
def get_badges(db: Session = Depends(database.get_db)):
    badges = db.query(models.Badge).all()
    return badges

@router.get("/{id}", response_model=schemas.BadgeResponse)
def get_badge_by_id(id: int, db: Session = Depends(database.get_db)):
    badge = db.query(models.Badge).filter(models.Badge.id == id).first()
    
    if not badge:
        raise HTTPException(status_code=404, detail="Badge não encontrado")
    
    return badge

@router.post("/alunos/{matricula}/badges/{badge_id}")
def conquistar_badge(matricula: str, badge_id: int, db: Session = Depends(database.get_db)):
    conquista = AlunoBadge(
        aluno_matricula_fk=matricula,
        badge_id_fk=badge_id, 
        data_conquista=date.today()
    )
    
    db.add(conquista)
    db.commit()
    return {"msg": "Badge conquistado com sucesso"}