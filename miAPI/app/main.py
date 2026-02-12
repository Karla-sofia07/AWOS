from fastapi import FastAPI
import asyncio
from typing import Optional

app= FastAPI(
    title="Mi primer API",
    description="Karla Sofía Álvarez Olguín",
    version="1.0.0"
    )

#TB ficticia
usuarios=[
    {"id":1, "nombre":"Montse", "edad": 20},
    {"id":2, "nombre":"Karla", "edad": 19},
    {"id":3, "nombre":"Pilar", "edad": 19},
]

#Endpoint
@app.get("/", tags=["Inicio"]) 
async def bienvenida():
    return {"message": "Bienvenido a mi API"}

@app.get("/HolaMundo", tags=["Bienvenida Asincrona"]) #Endpoint
async def hola():
    await asyncio.sleep(3)
    return {"mensaje": "Hola Mundo FAstAPI" ,
            "estatus" : "200"
            } #formato json

@app.get("/v1/usuario/{id}" ,tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario" : id }

@app.get("/v1/usuarios/" ,tags=['Parametro Opcional'])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario": usuario}
        return {"mensaje": "Usuario no encontrado"}
    return {"mensaje": "usuario no encontrado" , "usuario":id}