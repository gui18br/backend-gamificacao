from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router  = APIRouter(prefix="/alunos", tags=["Users"])

@router.put("registrar/{aluno_id}", response_model=schemas.AlunoResponse)
def register_aluno(aluno_id: int, aluno_data: schemas.AlunoRegister, db: Session = Depends(database.get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    update_data = aluno_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_aluno, key, value)
        
    db.commit()
    db.refresh(db_aluno)
    return db_aluno