from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.models.aluno import Aluno
from app.models.turma import Turma

router  = APIRouter(prefix="/turmas", tags=["Turmas"])

@router.post("/", response_model=schemas.TurmaResponse)
def create_turma(turma: schemas.TurmaCreate, db: Session = Depends(database.get_db)):

    prof = None
    if turma.professor_id_fk:
        prof = db.query(models.Professor).filter(models.Professor.id == turma.professor_id_fk).first()
        if not prof:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    new_turma = models.Turma(nome=turma.nome, professor_id_fk=prof)
    db.add(new_turma)
    db.commit()
    db.refresh(new_turma)
    
    return new_turma
    
@router.get("/", response_model=List[schemas.TurmaBase])
def get_turmas(db: Session = Depends(database.get_db)):
    turmas = db.query(models.Turma).all()
    return turmas

@router.get("/{id}", response_model=schemas.TurmaResponse)
def get_turma_by_id(id: int, db: Session = Depends(database.get_db)):
    turma = db.query(models.Turma).filter(models.Turma.id == id).first()
    
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    return turma

@router.post("/alunos/{matricula}/turmas/{turma_id}")
def add_aluno_turma(matricula: str, turma_id: int, db: Session = Depends(database.get_db)):
    aluno = db.get(Aluno, matricula)
    turma = db.get(Turma, turma_id)
    aluno.turmas.append(turma)
    db.commit()
    return {"msg": f"Aluno {aluno.nome} adicionado à turma {turma.nome}"}

@router.get("alunos/{matricula}/turmas")
def listar_turmas_aluno(matricula: str, db: Session = Depends(database.get_db)):
    aluno = db.get(Aluno, matricula)
    return aluno.turmas