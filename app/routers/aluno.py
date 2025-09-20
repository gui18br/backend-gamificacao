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
    
    hashed_pwd = hash_password(aluno.senha)
    new_aluno = models.Aluno(matricula=aluno.matricula, senha=hashed_pwd, nickname=aluno.nickname, nome=aluno.nome, icone=aluno.icone)
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
    