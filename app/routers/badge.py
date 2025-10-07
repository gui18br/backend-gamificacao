from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.schemas import badge as schemas
from app.models.badge import Badge

from app.models.aluno_badge import AlunoBadge

router  = APIRouter(prefix="/badges", tags=["Badges"])

@router.post('/', response_model=schemas.BadgeResponseSingle)
def create_badge(badge: schemas.BadgeCreate, db: Session = Depends(database.get_db)):
    
    new_badge = Badge(
        nome=badge.nome,
        requisito=badge.requisito,
        icone=badge.icone
    )
    
    db.add(new_badge)
    db.commit()
    db.refresh(new_badge)
    
    return {"data": new_badge}

@router.get("/", response_model=schemas.BadgeResponseList)
def get_badges(db: Session = Depends(database.get_db)):
    badges = db.query(Badge).all()
    return {"data": badges}

@router.get("/{id}", response_model=schemas.BadgeResponseSingle)
def get_badge_by_id(id: int, db: Session = Depends(database.get_db)):
    badge = db.query(Badge).filter(Badge.id == id).first()
    
    if not badge:
        raise HTTPException(status_code=404, detail="Badge não encontrado")
    
    return {"data": badge}

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