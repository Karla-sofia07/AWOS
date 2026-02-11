#Importaciones
from fastapi import FastAPI
import asyncio 
from typing import Optional 
#Instacia 
app = FastAPI(
    title='Mi primer API',
    description='Karla Sofía Álvarez Olguín',
    version='1.0.0'
    )

#BD ficticia
usuarios= [
    {"id":1"nombre":"Juan","edad":21},
    {"id":2"nombre":"Israel","edad":21},
    {"id":1"nombre":"Sofi","edad":21},
]

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


@app.get("/v1/usuario/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontró usuario": id}


@app.get("/v1/usuario/", tags=['Parametro Opcional'])
async def consultaUno(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios: 
            if  usuario["id"] == id: 
                return {"mensaje": "usuario encontrado", "usuario":usuario}
       return {"mensaje": "usuario encontrado", "usuario":id} 
    else:    
        return {"mensaje": "No se proporcionó id"}