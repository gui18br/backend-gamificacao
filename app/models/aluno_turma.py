from sqlalchemy import String, Table, Column, Integer, ForeignKey
from .database import Base

aluno_turma = Table(
    "aluno_turma",
    Base.metadata,
    Column("aluno_matricula_fk", String, ForeignKey("Aluno.matricula"), primary_key=True),
    Column("turma_id_fk", Integer, ForeignKey("Turma.id"), primary_key=True)
)
