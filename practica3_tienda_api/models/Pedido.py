from uuid import uuid4
from datetime import datetime

from .Usuario import Cliente
from .Producto import Producto

class Pedido:
    """
    Representa un pedido realizado por un cliente.
    identificador único (string, uuid4)
    instancia de Cliente
    lineas: lista de tuplas (Producto, cantidad > 0)
    fecha: fecha/hora del pedido (datetime)
    """

    def __init__(self, cliente, lineas=None, fecha=None, id_=None):
        #Validaciones básicas
        if not isinstance(cliente, Cliente):
            raise TypeError("El pedido debe estar vinculado a un Cliente.")

        self.id = id_ or str(uuid4())
        self.cliente = cliente
        self.fecha = fecha or datetime.now()

        #Normalizamos y validamos las líneas
        self.lineas = []
        if lineas:
            for prod, cant in lineas:
                if not isinstance(prod, Producto):
                    raise TypeError("Cada línea debe incluir un Producto válido.")
                cant = int(cant)
                if cant <= 0:
                    raise ValueError("La cantidad debe ser positiva.")
                self.lineas.append((prod, cant))

    #Cálculo del total Importe total = suma de (precio * cantidad) en cada línea
    def calcular_total(self):
        total = 0.0
        for prod, cant in self.lineas:
            total += float(prod.precio) * int(cant)
        return total

    def __str__(self):
        cabecera = f"Pedido {self.id} | {self.fecha:%Y-%m-%d %H:%M} | Cliente: {self.cliente.nombre}"
        detalle = " | ".join(f"{p.nombre} x{cant}" for p, cant in self.lineas) or "(sin líneas)"
        return f"{cabecera}\n  {detalle}\n  TOTAL: {self.calcular_total():.2f}€"