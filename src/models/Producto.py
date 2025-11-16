from uuid import uuid4

class Producto:
    """
    Clase base para todos los productos de la tienda.
    identificador único (string) generado automáticamente
    nombre: nombre del producto
    precio: precio unitario (>= 0)
    stock: unidades disponibles (>= 0)
    """
    def __init__(self, nombre, precio, stock, id_=None):
        precio = float(precio)
        stock = int(stock)
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.id = id_ or str(uuid4())
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    #Consultas y actualización de stock
    def hay_stock(self, cantidad):    #Devuelve True si hay al menos 'cantidad' unidades disponibles
        cantidad = int(cantidad)
        if cantidad < 0:
            raise ValueError("La cantidad solicitada no puede ser negativa.")
        return self.stock >= cantidad

    def actualizar_stock(self, delta):  #Ajusta el stock en 'delta' unidades (positivo o negativo)
        delta = int(delta)
        nuevo = self.stock + delta
        if nuevo < 0:
            raise ValueError(f"Stock insuficiente de '{self.nombre}'.")
        self.stock = nuevo

    #Representación
    def __str__(self):
        return f"[{self.id}] {self.nombre} - {self.precio:.2f}€ (stock: {self.stock})"


class ProductoElectronico(Producto):  #Producto electrónico con garantía en meses
    def __init__(self, nombre, precio, stock, garantia_meses, id_=None):
        super().__init__(nombre, precio, stock, id_)
        garantia_meses = int(garantia_meses)
        if garantia_meses < 0:
            raise ValueError("La garantía no puede ser negativa.")
        self.garantia_meses = garantia_meses

    def __str__(self):
        return f"{super().__str__()} | garantía: {self.garantia_meses} meses"


class ProductoRopa(Producto):  #Producto de ropa con talla y color
    def __init__(self, nombre, precio, stock, talla, color, id_=None):
        super().__init__(nombre, precio, stock, id_)
        self.talla = talla
        self.color = color

    def __str__(self):
        return f"{super().__str__()} | talla: {self.talla}, color: {self.color}"
