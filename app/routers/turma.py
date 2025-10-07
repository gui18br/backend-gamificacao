from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.schemas import turma as schemas
from app.models import turma as models
from app.models.aluno import Aluno
from app.models.turma import Turma
from app.models.professor import Professor
from app.security import get_current_user

router  = APIRouter(prefix="/turmas", tags=["Turmas"])

@router.post("/", response_model=schemas.TurmaResponseSingle)
def create_turma(turma: schemas.TurmaCreate, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):

    prof = None
    if turma.professor_matricula_fk:
        prof = db.query(Professor).filter(Professor.matricula == turma.professor_matricula_fk).first()
        if not prof:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    new_turma = Turma(
        nome=turma.nome,
        professor_matricula_fk=prof.matricula
    )
    
    db.add(new_turma)
    db.commit()
    db.refresh(new_turma)
    
    return {"data": new_turma}
    
@router.get("/", response_model=schemas.TurmaResponseList)
def get_turmas(db: Session = Depends(database.get_db)):
    turmas = db.query(Turma).all()
    return {"data":turmas}

@router.get("/{id}", response_model=schemas.TurmaResponseSingle)
def get_turma_by_id(id: int, db: Session = Depends(database.get_db)):
    turma = db.query(Turma).filter(Turma.id == id).first()
    
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    return {"data":turma}

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