from models.Usuario import Usuario, Cliente, Administrador
from models.Producto import Producto, ProductoElectronico, ProductoRopa
from models.Pedido import Pedido


class TiendaService:  #Servicio principal de la tienda online
    def __init__(self):
        self._usuarios = {}   #idUsuario
        self._productos = {}  #idProducto
        self._pedidos = []    #lista de Pedido

    #Registro y gestión de usuarios. Tipo: 'cliente' o 'admin'
    def registrar_usuario(self, tipo, nombre, email, direccion=None):
        t = (tipo or "").lower().strip()

        if t == "cliente":
            if not direccion:
                raise ValueError("Para registrar un cliente debes indicar la dirección.")
            usuario = Cliente(nombre, email, direccion)
        elif t in ("admin", "administrador"):
            usuario = Administrador(nombre, email)
        else:
            raise ValueError("Tipo de usuario no soportado (usa 'cliente' o 'admin').")

        self._usuarios[usuario.id] = usuario
        return usuario

    def get_usuario(self, usuario_id):  #Obtiene un usuario por id
        
        return self._usuarios.get(usuario_id)

    def listar_usuarios(self):
        """
        Devuelve una lista con todos los usuarios registrados.
        """
        return list(self._usuarios.values())


    #Productos

    def anadir_producto_generico(self, nombre, precio, stock):
        """
        Crea y almacena un Producto genérico.
        """
        p = Producto(nombre, precio, stock)
        self._productos[p.id] = p
        return p

    def anadir_producto_electronico(self, nombre, precio, stock, garantia_meses):   #Crea y almacena un ProductoElectronico
       
        p = ProductoElectronico(nombre, precio, stock, garantia_meses)
        self._productos[p.id] = p
        return p

    def anadir_producto_ropa(self, nombre, precio, stock, talla, color):   #Crea y almacena un ProductoRopa

        p = ProductoRopa(nombre, precio, stock, talla, color)
        self._productos[p.id] = p
        return p

    def eliminar_producto(self, producto_id):  #Elimina un producto por id

        return self._productos.pop(producto_id, None) is not None

    def listar_productos(self):  #Devuelve la lista de productos del inventario
    
        return list(self._productos.values())

    def get_producto(self, producto_id):   #Objetiene un producto por id
    
        return self._productos.get(producto_id)

    # Pedido para un usuario (cliente) con items. Valida y actualiza stock, crea y almacena el Pedido
    def realizar_pedido(self, usuario_id, items):
        usuario = self._usuarios.get(usuario_id)
        if usuario is None:
            raise ValueError("Usuario no encontrado.")
        if not isinstance(usuario, Cliente):
            raise ValueError("Solo un Cliente puede realizar pedidos.")

        # Preparar líneas y chequear stock
        lineas = []
        for prod_id, cantidad in items:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser positiva.")
            prod = self._productos.get(prod_id)
            if prod is None:
                raise ValueError(f"Producto {prod_id} no encontrado.")
            if not prod.hay_stock(cantidad):
                raise ValueError(f"Stock insuficiente de '{prod.nombre}'.")
            lineas.append((prod, cantidad))

        # Descontar stock
        for prod, cant in lineas:
            prod.actualizar_stock(-cant)

        pedido = Pedido(usuario, lineas)
        self._pedidos.append(pedido)
        return pedido

    def listar_pedidos_por_usuario(self, usuario_id):   #lista los pedidos de un usuario
        pedidos = [p for p in self._pedidos if p.cliente.id == usuario_id]
        return sorted(pedidos, key=lambda p: p.fecha)