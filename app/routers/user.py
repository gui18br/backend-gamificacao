from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router  = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.matricula == user.matricula).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Matricula já registrada")
    
    new_user = models.Usuario(nome=user.nome, senha=user.senha, icone=user.icone, tipo=user.tipo)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    if user.tipo == 'aluno':
        new_aluno = models.Aluno()
        db.add(new_aluno)
    else: 
        new_prof = models.Professor()
        db.add(new_prof)
        
    db.commit()
    db.refresh(new_user)
    return new_user
    