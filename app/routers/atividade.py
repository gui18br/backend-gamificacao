from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.models.aluno_atividade import AlunoAtividade

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

    
    new_atv = models.Atividade(nome=atv.nome, nota_max=atv.nota_max, pontos=atv.pontos, badge_id_fk=badge, turma_id_fk=atv.turma, data_entrega=atv.data_entrega)
    db.add(new_atv)
    db.commit()
    db.refresh(new_atv)
    
    return new_atv
    
@router.get("/", response_model=List[schemas.AtividadeBase])
def get_atvs(db: Session = Depends(database.get_db)):
    atvs = db.query(models.Atividade).all()
    return atvs

@router.get("/{id}", response_model=schemas.AtividadeResponse)
def get_atv_by_id(id: int, db: Session = Depends(database.get_db)):
    atv = db.query(models.Atividade).filter(models.Atividade.id == id).first()
    
    if not atv:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    return atv

@router.post("/alunos/{matricula}/atividades/{atv_id}")
def atribuir_nota_aluno(matricula: str, atv_id: int, nota: str, db: Session = Depends(database.get_db)):
    atv_com_nota = AlunoAtividade(
        aluno_matricula_fk=matricula,
        atividade_id_fk=atv_id,
        nota=nota
    )
    
    db.add(atv_com_nota)
    db.commit()
    return {"msg": f"Nota da atividade {atv_id} atribuída ao aluno {matricula}"}
    