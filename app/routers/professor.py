from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from datetime import timedelta
from app.security import hash_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router  = APIRouter(prefix="/professores", tags=["Profs"])

@router.post("/", response_model=schemas.ProfessorResponse)
def create_user(professor: schemas.ProfessorCreate, db: Session = Depends(database.get_db)):
    db_prof = db.query(models.Professor).filter(models.Professor.matricula == professor.matricula).first()
    if db_prof:
        raise HTTPException(status_code=400, detail="matricula já registrada")
    
    avatar = None
    if professor.avatar_id:
        avatar = db.query(models.Avatar).filter(models.Avatar.id == professor.avatar_id).first()
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar não encontrado")
    
    hashed_pwd = hash_password(professor.senha)
    new_user = models.Usuario(matricula=professor.matricula, nome=professor.nome, senha=hashed_pwd, avatar_id=professor.avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.id)}, 
        expires_delta=access_token_expires
    )
    
    return {
        "id": new_user.id,
        "access_token": f"bearer {access_token}",
    }
    
@router.get("/", response_model=List[schemas.ProfessorBase])
def get_atvs(db: Session = Depends(database.get_db)):
    professores = db.query(models.Professor).all()
    return professores

@router.get("/{matricula}", response_model=schemas.AlunoResponse)
def get_prof_by_id(matricula: int, db: Session = Depends(database.get_db)):
    prof = db.query(models.Professor).filter(models.Professor.matricula == matricula).first()
    
    if not prof:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    return prof
    