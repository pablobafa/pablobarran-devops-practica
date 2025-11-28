from typing import List

from fastapi import FastAPI, HTTPException, status
from Services.Tienda_service import TiendaService
from schemas import UsuarioCreate, UsuarioRead

# Crear la app de FastAPI
app = FastAPI(
    title="Tienda Online - Práctica 3",
    version="1.0.0",
)

# Instancia global de la lógica de negocio
tienda = TiendaService()

def usuario_to_read(usuario) -> UsuarioRead:
    """
    Convierte un objeto Usuario / Cliente / Administrador en un schema UsuarioRead.
    """
    # Determinar tipo y dirección
    tipo = "admin" if usuario.is_admin() else "cliente"
    direccion = getattr(usuario, "direccion", None)

    return UsuarioRead(
        id=str(usuario.id),
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.is_admin(),
        tipo=tipo,
        direccion=direccion,
    )


@app.get("/")
def root():
    """Endpoint sencillo para comprobar que la API funciona."""
    return {"mensaje": "API de la tienda online funcionando"}


@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioCreate):
    """
    Crea un nuevo usuario (cliente o admin) usando TiendaService.
    """
    try:
        usuario = tienda.registrar_usuario(
            datos.tipo,
            datos.nombre,
            datos.email,
            datos.direccion,
        )
    except ValueError as e:
        # Errores de validación de tu lógica (tipo incorrecto, dirección vacía, etc.)
        raise HTTPException(status_code=400, detail=str(e))

    return usuario_to_read(usuario)

@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios():
    """
    Devuelve todos los usuarios registrados en la tienda.
    """
    usuarios = tienda.listar_usuarios()  # usa el método que añadimos en TiendaService
    return [usuario_to_read(u) for u in usuarios]

@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: str):
    """
    Devuelve un usuario concreto por su id.
    """
    # usamos el método de servicio que ya tenías
    usuario = tienda.get_usuario(usuario_id)

    if usuario is None:
        # si no existe, devolvemos un 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario_to_read(usuario)