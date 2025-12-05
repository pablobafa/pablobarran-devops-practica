from typing import Literal, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

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

    # ======== SCHEMAS DE PRODUCTO ======== #

class ProductoCreate(BaseModel):
    """
    Datos necesarios para crear un producto.
    tipo:
      - 'generico'     -> Producto normal
      - 'electronico'  -> ProductoElectronico (usa garantia_meses)
      - 'ropa'         -> ProductoRopa (usa talla y color)
    """
    tipo: Literal["generico", "electronico", "ropa"]
    nombre: str
    precio: float
    stock: int

    # Atributos específicos según tipo
    garantia_meses: Optional[int] = None  # solo para electrónicos
    talla: Optional[str] = None           # solo para ropa
    color: Optional[str] = None           # solo para ropa


class ProductoRead(BaseModel):
    """
    Datos que devolvemos al cliente al consultar productos.
    """
    id: str
    tipo: Literal["generico", "electronico", "ropa"]
    nombre: str
    precio: float
    stock: int

    garantia_meses: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None

    
# ----- PEDIDOS -----

class PedidoItemCreate(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0, description="Cantidad del producto (>= 1)")


class PedidoCreate(BaseModel):
    cliente_id: str
    items: List[PedidoItemCreate]


class PedidoItemRead(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float


class PedidoRead(BaseModel):
    id: str
    fecha: datetime
    cliente_id: str
    cliente_nombre: str
    total: float
    items: List[PedidoItemRead]