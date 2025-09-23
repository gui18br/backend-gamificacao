from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from datetime import timedelta
from app.security import hash_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router  = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.post("/", response_model=schemas.AlunoResponse)
def create_user(aluno: schemas.AlunoCreate, db: Session = Depends(database.get_db)):
    db_aluno = db.query(models.ALuno).filter(models.User.matricula == aluno.matricula).first()
    if db_aluno:
        raise HTTPException(status_code=400, detail="Matricula já registrada")
    
    avatar = None
    if aluno.avatar_id_fk:
        avatar = db.query(models.Avatar).filter(models.Avatar.id == aluno.avatar_id_fk).first()
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar não encontrado")
    
    hashed_pwd = hash_password(aluno.senha)
    new_aluno = models.Aluno(matricula=aluno.matricula, senha=hashed_pwd, nickname=aluno.nickname, nome=aluno.nome, xp=aluno.xp,nivel=aluno.nivel,avatar_id_fk=aluno.avatar_id_fk,)
    db.add(new_aluno)
    db.commit()
    db.refresh(new_aluno)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_aluno.id)}, 
        expires_delta=access_token_expires
    )
    
    return {
        "matricula": new_aluno.matricula,
        "access_token": f"bearer {access_token}",
    }
    
@router.get("/", response_model=List[schemas.AlunoBase])
def get_atvs(db: Session = Depends(database.get_db)):
    alunos = db.query(models.Aluno).all()
    return alunos

@router.get("/{matricula}", response_model=schemas.AlunoResponse)
def get_aluno_by_id(matricula: int, db: Session = Depends(database.get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.matricula == matricula).first()
    
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    return aluno