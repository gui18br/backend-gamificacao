from datetime import timedelta
from app import database
from app.models.aluno import Aluno
from app.schemas import login as schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/aluno", response_model=schemas.LoginAlunoResponse)
def login_aluno(aluno: schemas.LoginAlunoBase, db: Session = Depends(database.get_db)):
    db_aluno = db.query(Aluno).filter(Aluno.matricula == aluno.matricula).first()
    
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Matricula não registrada")
    
    senha_corresponde = verify_password(plain_password=aluno.senha, hashed_password=db_aluno.senha)
    
    if not senha_corresponde:
        raise HTTPException(status_code=401, detail="Usuário e/ou senha incorretas.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_aluno.matricula)},
        expires_delta=access_token_expires
    )
    
    return {
        "data": {
            "matricula": aluno.matricula, "access_token": access_token
        }
    }