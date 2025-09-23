from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router  = APIRouter(prefix="/atividades", tags=["Atividades"])

@router.post("/", response_model=schemas.AtividadeResponse)
def create_atv(atv: schemas.AtividadeCreate, db: Session = Depends(database.get_db)):
    
    badge = None
    if atv.badge_id_fk:
        badge = db.query(models.Badge).filter(models.Badge.id == atv.badge_id_fk).first()
        if not badge:
            raise HTTPException(status_code=404, detail="Badge não encontrada")

    turma = None
    if atv.turma_id_fk:
        turma = db.query(models.Turma).filter(models.Turma.id == atv.Turma_id_fk).first()
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")

    
    new_atv = models.Atividade(nome=atv.nome, nota_max=atv.nota_max, pontos=atv.pontos, badge_id_fk=badge, turma_id_fk=atv.turma)
    db.add(new_atv)
    db.commit()
    db.refresh(new_atv)
    
    return new_atv
    
@router.get("/", response_model=List[schemas.AtividadeBase])
def get_atvs(db: Session = Depends(database.get_db)):
    atvs = db.query(models.Atividades).all()
    return atvs

@router.get("/{id}", response_model=schemas.AtividadeResponse)
def get_atv_by_id(id: int, db: Session = Depends(database.get_db)):
    atv = db.query(models.Atividade).filter(models.Atividade.id == id).first()
    
    if not atv:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    return atv
    