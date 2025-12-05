from typing import List

from fastapi import FastAPI, HTTPException, status
from Services.Tienda_service import TiendaService
from schemas import (
    UsuarioCreate,
    UsuarioRead,
    ProductoCreate,
    ProductoRead,
    PedidoCreate,
    PedidoRead,
    PedidoItemRead,
)
from models.Pedido import Pedido
from datetime import datetime
from uuid import uuid4

# Crear la app de FastAPI
app = FastAPI(
    title="Tienda Online - Práctica 3",
    version="1.0.0",
)

# Instancia global de la lógica de negocio
tienda = TiendaService()


def usuario_to_read(usuario) -> UsuarioRead:
    """Convierte un objeto Usuario / Cliente / Administrador en un schema UsuarioRead."""
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


def producto_to_read(producto) -> ProductoRead:
    """Convierte un producto de dominio en ProductoRead detectando el tipo."""
    garantia_meses = getattr(producto, "garantia_meses", None)
    talla = getattr(producto, "talla", None)
    color = getattr(producto, "color", None)

    if garantia_meses is not None:
        tipo = "electronico"
    elif talla is not None or color is not None:
        tipo = "ropa"
    else:
        tipo = "generico"

    return ProductoRead(
        id=str(producto.id),
        tipo=tipo,
        nombre=producto.nombre,
        precio=float(producto.precio),
        stock=int(producto.stock),
        garantia_meses=garantia_meses,
        talla=talla,
        color=color,
    )


def pedido_to_read(pedido: Pedido) -> PedidoRead:
    """Convierte un objeto Pedido de dominio en un schema PedidoRead."""
    items_read: list[PedidoItemRead] = []

    # Suponemos que pedido.lineas es una lista de tuplas (producto, cantidad)
    for producto, cantidad in pedido.lineas:
        subtotal = producto.precio * cantidad
        items_read.append(
            PedidoItemRead(
                producto_id=str(producto.id),
                nombre=producto.nombre,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal,
            )
        )

    total = sum(item.subtotal for item in items_read)

    return PedidoRead(
        id=str(pedido.id),
        fecha=pedido.fecha,
        cliente_id=str(pedido.cliente.id),
        cliente_nombre=pedido.cliente.nombre,
        total=total,
        items=items_read,
    )


@app.get("/")
def root():
    return {"mensaje": "API de la tienda online funcionando"}


# ---------- USUARIOS ----------

@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioCreate):
    try:
        usuario = tienda.registrar_usuario(
            datos.tipo,
            datos.nombre,
            datos.email,
            datos.direccion,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return usuario_to_read(usuario)


@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios():
    usuarios = tienda.listar_usuarios()
    return [usuario_to_read(u) for u in usuarios]


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: str):
    usuario = tienda.get_usuario(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_to_read(usuario)


# ---------- PRODUCTOS ----------

@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate):
    t = datos.tipo

    try:
        if t == "generico":
            producto = tienda.anadir_producto_generico(
                datos.nombre,
                datos.precio,
                datos.stock,
            )
        elif t == "electronico":
            if datos.garantia_meses is None:
                raise ValueError("Para un producto electrónico debes indicar garantia_meses.")
            producto = tienda.anadir_producto_electronico(
                datos.nombre,
                datos.precio,
                datos.stock,
                datos.garantia_meses,
            )
        elif t == "ropa":
            if not datos.talla or not datos.color:
                raise ValueError("Para un producto de ropa debes indicar talla y color.")
            producto = tienda.anadir_producto_ropa(
                datos.nombre,
                datos.precio,
                datos.stock,
                datos.talla,
                datos.color,
            )
        else:
            raise ValueError("Tipo de producto no soportado.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return producto_to_read(producto)


@app.get("/productos", response_model=List[ProductoRead])
def listar_productos():
    productos = tienda.listar_productos()
    return [producto_to_read(p) for p in productos]


@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: str):
    producto = tienda.get_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto_to_read(producto)


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: str):
    borrado = tienda.eliminar_producto(producto_id)
    if not borrado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None


@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido_data: PedidoCreate):
    # 1. Comprobar que el cliente existe
    cliente = tienda.get_usuario(pedido_data.cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    # 2. Preparar las líneas del pedido: comprobar producto y stock
    lineas: list[tuple] = []
    for item in pedido_data.items:
        producto = tienda.get_producto(item.producto_id)
        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {item.producto_id} no encontrado",
            )

        if producto.stock < item.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para el producto {producto.nombre}",
            )

        lineas.append((producto, item.cantidad))

    # 3. Crear el pedido (sin usar tienda.crear_pedido, que NO existe)

    #  Esto NO llama a __init__, así evitamos problemas si tu constructor tiene otra firma
    pedido = Pedido.__new__(Pedido)
    pedido.id = uuid4()
    pedido.cliente = cliente
    pedido.fecha = datetime.now()
    pedido.lineas = []

    # Añadimos las líneas y actualizamos stock
    for producto, cantidad in lineas:
        pedido.lineas.append((producto, cantidad))
        producto.stock -= cantidad

    # Guardamos el pedido en la tienda
    if not hasattr(tienda, "pedidos"):
        tienda.pedidos = []   # por si acaso, pero casi seguro ya existe

    tienda.pedidos.append(pedido)

    # 4. Devolverlo convertido a schema
    return pedido_to_read(pedido)



@app.get("/usuarios/{cliente_id}/pedidos", response_model=list[PedidoRead])
def listar_pedidos_cliente(cliente_id: str):
    # Comprobar que el cliente existe
    cliente = tienda.get_usuario(cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    # Filtrar los pedidos de ese cliente
    pedidos_cliente: list[PedidoRead] = []
    if hasattr(tienda, "pedidos"):
        for pedido in tienda.pedidos:
            if str(pedido.cliente.id) == cliente_id:
                pedidos_cliente.append(pedido_to_read(pedido))

    return pedidos_cliente

