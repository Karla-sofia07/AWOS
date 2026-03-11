# IMPORTACIONES
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Instacia 
app = FastAPI(
    title='API Sistema de tickets de soporte técnico',
     description='Sofía Álvarez',
     version='1.0.0'
     ) 

# Base de datos ficticia
tickets = []
estados = []
# modelos
class Usuario(BaseModel):
    nombre: str = Field(..., min_length=5, max_length=200)
    correo: EmailStr

class Ticket(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=20, max_length=200)
    autor: str
    estado: str = Field(default="Pendiente", pattern="^(Pendiente|Pendiente)$")

class Estado(BaseModel):
    ticket_id: int

# MODELO PYDANTIC
class UsuarioCreate(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 - 123")


# ENDPOINTS

#bienvenida
@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"mensaje": "¡Bienvenido a la gestión de tickets!"}

#crear ticket
@app.post("/libros/", status_code=status.HTTP_201_CREATED)
def Crear_ticket(Ticket: Ticket):

    for l in libros:
        if l["id"] == ticket.id:
            raise HTTPException(status_code=400, detail="Este ticket ya existe")

    tickets.append(Ticket.dict())
    return {"mensaje": "Ticket creado correctamente"}

#listar tickets
@app.get("/tickets/")
def listar_tickets():
    return tickets

#consultar ID
@app.get("/v1/ticket/{id}", tags=['Parametro Obligatorio'])
async def ConsultarID(
    id:int
      userAuth: str = Depends(verificar_peticion)
    ):
     for index, usr in enumerate(tickets):
     if usr["id"] == id:
       tickets.pop(index)
    return {
         "mensaje": "ticket encontrado por: {userAuth}": id
        }


@app.get("/v1/ticket/{id}", tags=['Parametro Obligatorio'])
async def ConsultarID(
    id:Optional[int]=None
    
    ):
    if id is not None:
        for Ticket in tickets: 
            if  usuario["id"] == id: 
                return {"mensaje": "ticket encontrado", "ticket":ticket}
       return {"mensaje": "ticket encontrado", "ticket":id} 
    else:    
        return {"mensaje": "No se proporcionó id"}
#cambiar estado

@app.put("/estado/cambiar/{ticket_id}")
def cambiar_estado(Ticket_id: int):

    estado = next((p for p in estados if p["ticket_id"] == ticket_id), None)

    if not estado:
        raise HTTPException(status_code=409, detail="El ticket no existe")

    ticket = next((l for l in tickets if l["id"] == ticket_id), None)
    ticket["estado"] = "disponible"

    tickets.remove(ticket)

    return {"mensaje": "Estado cambiado correctamente"}

#eliminar ticket
@app.delete("/ticket/{ticket_id}")
def eliminar_ticket(ticket_id: int):

    ticket = next((p for p in tickets if p["ticket_id"] == ticket_id), None)

    if not ticket:
        raise HTTPException(status_code=409, detail="El registro no existe")

    tickets.remove(ticket)

    return {"mensaje": "Ticket eliminado"}
