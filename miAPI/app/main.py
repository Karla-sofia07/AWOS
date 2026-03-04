# IMPORTACIONES
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


# INSTANCIA DE LA APP

app = FastAPI(
    title="Mi primer API",
    description="Esta es mi primera API con FastAPI en la clase del profe Isay",
    version="1.0.0"
)


# SEGURIDAD HTTP BASIC
security = HTTPBasic()

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credentials.username, "Sofia")
    passAuth = secrets.compare_digest(credentials.password, "123456")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )

    return credentials.username


# BASE DE DATOS FICTICIA
usuarios = [
    {"id": 1, "nombre": "Montse", "edad": 20},
    {"id": 2, "nombre": "Jairo", "edad": 20},
    {"id": 3, "nombre": "Pilar", "edad": 19},
    {"id": 4, "nombre": "Alexis", "edad": 20}
]



# MODELO PYDANTIC

class UsuarioCreate(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 - 123")



# ENDPOINTS

@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"message": "Bienvenido a mi API"}


@app.get("/HolaMundo", tags=["Bienvenida Asincrona"])
async def hola():
    await asyncio.sleep(3)
    return {
        "mensaje": "Hola Mundo FastAPI",
        "estatus": "200"
    }


@app.get("/v1/parametroOb/{id}", tags=["Parametro Obligatorio"])
async def consulta_uno(id: int):
    return {"Se encontro usuario": id}


@app.get("/v1/parametroOp/", tags=["Parametro opcional"])
async def consulta_todos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuario}
        return {"mensaje": "usuario no encontrado", "usuario": id}
    else:
        return {"mensaje": "No se proporciono id"}



# CRUD

@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def leer_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }


@app.post(
    "/v1/usuarios/",
    tags=["CRUD HTTP"],
    status_code=status.HTTP_201_CREATED
)
async def crear_usuario(usuario: UsuarioCreate):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado",
        "usuario": usuario
    }


@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, usuario: UsuarioCreate):
    for i, u in enumerate(usuarios):
        if u["id"] == id:
            usuarios[i] = usuario.dict()
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuario
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(
    id: int,
    userAuth: str = Depends(verificar_peticion)
):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por: {userAuth}"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )