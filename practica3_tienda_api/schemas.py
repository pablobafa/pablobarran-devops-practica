from typing import Literal, Optional
from pydantic import BaseModel, EmailStr

# ======== SCHEMAS DE USUARIO ======== #

class UsuarioCreate(BaseModel):
    """
    Datos necesarios para crear un usuario desde la API.
    """
    # Tipo decide si se crea un Cliente o un Administrador
    tipo: Literal["cliente", "admin"]
    nombre: str
    email: EmailStr
    direccion: str  # el enunciado pide dirección postal (para clientes)


class UsuarioRead(BaseModel):
    """
    Datos que devuelve la API cuando consultamos un usuario.
    Cumple con el enunciado: id, nombre, email, es_admin.
    Añadimos tipo y direccion como información extra.
    """
    id: str
    nombre: str
    email: EmailStr
    es_admin: bool
    tipo: Literal["cliente", "admin"]
    direccion: Optional[str] = None