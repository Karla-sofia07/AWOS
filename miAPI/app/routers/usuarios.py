# ENDPOINTS

from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioCreate 
from app.data.database import usuarios
from app. security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB

router = APIRouter(
    prefix= "", tags= ["CRUD HTTP"]
) 

# CRUD
@router.get("/")
async def leer_usuarios(db:Session= Depends (get_db)):

    queryUsers= db.query(usuarioDB).all()

    return {
        "status": "200",
        "total": len( queryUsers),
        "usuarios": queryUsers
    }

@router.post("/" , status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP: UsuarioCreate, db:Session= Depends(get_db)):

    nuevoUsuario= usuarioDB(nombre=usuarioP.nombre, edad= usuarioP.edad)
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)


    return {
        "mensaje": "Usuario agregado",
        "usuario": usuarioP
    }


@router.put("/{id}")
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


@router.delete("/{id}")
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
