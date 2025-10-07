from fastapi import FastAPI
from app.routers import aluno, atividade, avatar, badge, login, professor, turma


app = FastAPI()

app.include_router(aluno.router)
app.include_router(atividade.router)
app.include_router(avatar.router)
app.include_router(badge.router)
app.include_router(professor.router)
app.include_router(turma.router)
app.include_router(login.router)

@app.get("/")
def root():
    return {"message": "API rodando com FastAPI 🚀"}
