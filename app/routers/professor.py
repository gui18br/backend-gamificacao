from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.schemas import professor as schemas
from app.models.professor import Professor
from app.models.avatar import Avatar
from datetime import timedelta
from app.security import hash_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router  = APIRouter(prefix="/professores", tags=["Profs"])

@router.post("/", response_model=schemas.ProfessorResponseCreate)
def create_user(professor: schemas.ProfessorCreate, db: Session = Depends(database.get_db)):
    db_prof = db.query(Professor).filter(Professor.matricula == professor.matricula).first()
    if db_prof:
        raise HTTPException(status_code=400, detail="matricula já registrada")
    
    avatar = None
    if professor.avatar_id_fk:
        avatar = db.query(Avatar).filter(Avatar.id == professor.avatar_id_fk).first()
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar não encontrado")
    
    hashed_pwd = hash_password(professor.senha)
    
    avatar_id = avatar.id if avatar else None
    
    new_user = Professor(
        matricula=professor.matricula,
        nome=professor.nome,
        senha=hashed_pwd,
        avatar_id_fk=avatar_id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.matricula)}, 
        expires_delta=access_token_expires
    )
    
    return {
        "data":   {
            "matricula": new_user.matricula,
            "access_token": f"bearer {access_token}",
        }
    }
    
@router.get("/", response_model=schemas.ProfessorResponseList)
def get_profs(db: Session = Depends(database.get_db)):
    professores = db.query(Professor).all()
    return {"data": professores}

@router.get("/{matricula}", response_model=schemas.ProfessorResponseSingle)
def get_prof_by_id(matricula: str, db: Session = Depends(database.get_db)):
    prof = db.query(Professor).filter(Professor.matricula == matricula).first()
    
    if not prof:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    return {"data": prof}
    