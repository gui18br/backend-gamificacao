from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from datetime import timedelta
from app.security import hash_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router  = APIRouter(prefix="/usuarios", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.matricula == user.matricula).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Matricula já registrada")
    
    hashed_pwd = hash_password(user.senha)
    new_user = models.Usuario(nome=user.nome, senha=hashed_pwd, icone=user.icone, tipo=user.tipo)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    if user.tipo == 'aluno':
        new_aluno = models.Aluno(id=new_user.id)
        db.add(new_aluno)
    else: 
        new_prof = models.Professor(id=new_user.id)
        db.add(new_prof)
        
    db.commit()
    db.refresh(new_user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.id)}, 
        expires_delta=access_token_expires
    )
    
    return {
        "id": new_user.id,
        "tipo_user": new_user.tipo,
        "access_token": f"bearer {access_token}",
    }
    