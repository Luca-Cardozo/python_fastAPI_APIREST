# API REST: Interfaz de programación de aplicaciones para compartir recursos


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

# inicializo una variable que tendrá todas las características de una API REST
app = FastAPI()

# defino el modelo


class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int


# simulo una base de datos
cursos_db = []

# CRUD
# Read (lectura): GET ALL -> Leo todos los cursos que hay en la db


@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

# Create (escribir): POST -> agrego un nuevo recurso a la db


@app.post("/cursos/", response_model=Curso)
def crear_curso(curso: Curso):
    curso.id = str(uuid.uuid4())  # genera un id único e irrepetible
    cursos_db.append(curso)
    return curso

# Read (lectura): GET (individual) -> Leo el curso que coincida con el id que yo pida


@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    # con next se toma la primera coincidencia del array
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# Update (actualizar/modificar): PUT (individual) -> modifico un recurso que coincida con el id que yo mande


@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: str, curso_actualizado: Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    # busco el índice donde está el curso en la lista (db)
    index = cursos_db.index(curso)
    cursos_db[index] = curso_actualizado
    return curso_actualizado


# Delete (borrado): DELETE (individual) -> elimino un recurso que coincida con el id que yo mande
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id: str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
