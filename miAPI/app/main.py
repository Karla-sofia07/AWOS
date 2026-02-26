#Importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio 
from typing import Optional 
from pydantic import BaseModel,Field

#Instacia 
app = FastAPI(
    title='Mi primer API',
     description='Sofía Álvarez',
     version='1.0.0'
     )
#TB ficticia 
usuarios=[
    {"id":1,"nombre":"Alexis","edad":20},
    {"id":2,"nombre":"America","edad":20},
    {"id":3,"nombre":"Jairo","edad":20},
]

#modelo de validacion
class usuario_create(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario, debe ser un entero positivo")
    nombre: str= Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=0, le=123, description="Edad valida entre 0 y 120")

#Endpoinst
@app.get("/", tags=['Inicio'])
async def bienvenida():
    return {"mensaje": "¡Bienvenido de mi API!"}

@app.get("/HolaMundo", tags=['Bienvenida Asincrona'])
async def hola():
    await asyncio.sleep(4) #Simulacion de una peticion
    return{
        "mensaje": "¡Hola mundo FastAPI!",
        "estatus": "200"
    }

@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario": id}

@app.get("/v1/parametroOp/", tags=['Parametro opcional'])
async def consultaTodos(id: Optional[int]= None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id: 
                return{"mensaje":"usuario encontrado", "usuario": usuario}
        return{"mensaje":"usuario no encontrado", "usuario": id}
    else:
        return{"mensaje":"No se proporciono id"}


@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return{
        "status":"200",
        "total": len(usuarios), 
        "usuarios":usuarios
    }


@app.post("/v1/usuarios/",tags=['CRUD HTTP'],status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: usuario_create):
    for Usr in usuarios:
        if Usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                 detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje": "Usuario agregado",
        "usuario": usuario
    }

@app.put("/v1/usuarios/{user_id}", tags=['CRUD HTTP'])
async def actualizar_usuario(user_id: int, datos: dict):
    for usr in usuarios:
        if usr["id"] == user_id:
            usr.update(datos)
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.delete("/v1/usuarios/{user_id}", tags=['CRUD HTTP'])
async def eliminar_usuario(user_id: int):
    for usr in usuarios:
        if usr["id"] == user_id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )