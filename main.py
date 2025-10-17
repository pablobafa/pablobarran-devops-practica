from Services.Tienda_service import TiendaService  

def imprimir_inventario(tienda: TiendaService, titulo: str) -> None:
    print(f"\n--- {titulo} ---")
    for p in tienda.listar_productos():
        print(p)

def main() -> None:
    tienda = TiendaService()  

    #Registro usuarios: 3 clientes + 1 admin 
    ana   = tienda.registrar_usuario("cliente", "Ana", "ana@gmail.com",   direccion="C/ Real, 123")
    luis  = tienda.registrar_usuario("cliente", "Luis", "luis@hotmail.com",  direccion="C/ Espana, 25")
    marta = tienda.registrar_usuario("cliente", "Marta", "marta@icloud.com", direccion="C/ Castilla C, 33")
    admin = tienda.registrar_usuario("admin",   "ADMIN", "admin@gmail.com")

    #Crear 5 productos de distintas categorías
    #Electrónicos
    auri   = tienda.anadir_producto_electronico("Auriculares", 29.90, 10, garantia_meses=24)
    raton   = tienda.anadir_producto_electronico("Ratón gamer", 19.50, 15, garantia_meses=12)
    # Ropa
    camiseta = tienda.anadir_producto_ropa("Camiseta", 12.00, 50, talla="M", color="Negro")
    sudadera = tienda.anadir_producto_ropa("Sudadera", 25.00, 20, talla="L", color="Azul")
    pantalon = tienda.anadir_producto_ropa("Pantalón", 35.00, 15, talla="M", color="Gris")

    #Listar productos para comprobar inventario 
    imprimir_inventario(tienda, "INVENTARIO INICIAL")

    #Simular 3 pedidos de clientes distintos
    print("\n--- PEDIDOS ---")
    pedido1 = tienda.realizar_pedido(ana.id,   [(auri.id, 2), (camiseta.id, 1)])
    print(pedido1, "\n")

    pedido2 = tienda.realizar_pedido(luis.id,  [(sudadera.id, 2)])
    print(pedido2, "\n")

    pedido3 = tienda.realizar_pedido(marta.id, [(raton.id, 1), (pantalon.id, 2)])
    print(pedido3, "\n")

    #Histórico de pedidos de un cliente 
    print("\n--- HISTÓRICO DE PEDIDOS DE ANA ---")
    for p in tienda.listar_pedidos_por_usuario(ana.id):
        print(p, "\n")

    #Stock actualizado tras los pedidos 
    imprimir_inventario(tienda, "INVENTARIO TRAS PEDIDOS")

if __name__ == "__main__":
    main()