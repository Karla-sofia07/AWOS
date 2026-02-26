from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital",
    description="Sofía Álvarez",
    version="1.0.0"
)

# Base de datos ficticia
libros = []
prestamos = []

# ----------- MODELOS -----------

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: EmailStr

class Libro(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    año: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: str = Field(default="disponible", pattern="^(disponible|prestado)$")

class Prestamo(BaseModel):
    libro_id: int
    usuario: Usuario

# ----------- ENDPOINTS -----------

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API Biblioteca Digital"}

# Registrar libro
@app.post("/libros/", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):

    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="El libro ya existe")

    libros.append(libro.dict())
    return {"mensaje": "Libro registrado correctamente"}

# Listar libros
@app.get("/libros/")
def listar_libros():
    return libros

# Buscar libro por nombre
@app.get("/libros/buscar/")
def buscar_libro(nombre: Optional[str] = None):

    if not nombre:
        raise HTTPException(status_code=400, detail="Debe proporcionar nombre")

    resultado = [l for l in libros if l["nombre"].lower() == nombre.lower()]

    if not resultado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return resultado

# Registrar préstamo
@app.post("/prestamos/")
def registrar_prestamo(prestamo: Prestamo):

    libro = next((l for l in libros if l["id"] == prestamo.libro_id), None)

    if not libro:
        raise HTTPException(status_code=404, detail="Libro no existe")

    if libro["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya está prestado")

    libro["estado"] = "prestado"
    prestamos.append(prestamo.dict())

    return {"mensaje": "Préstamo registrado"}

# Devolver libro
@app.put("/prestamos/devolver/{libro_id}")
def devolver_libro(libro_id: int):

    prestamo = next((p for p in prestamos if p["libro_id"] == libro_id), None)

    if not prestamo:
        raise HTTPException(status_code=409, detail="El registro no existe")

    libro = next((l for l in libros if l["id"] == libro_id), None)
    libro["estado"] = "disponible"

    prestamos.remove(prestamo)

    return {"mensaje": "Libro devuelto correctamente"}

# Eliminar préstamo
@app.delete("/prestamos/{libro_id}")
def eliminar_prestamo(libro_id: int):

    prestamo = next((p for p in prestamos if p["libro_id"] == libro_id), None)

    if not prestamo:
        raise HTTPException(status_code=409, detail="El registro no existe")

    prestamos.remove(prestamo)

    return {"mensaje": "Préstamo eliminado"}