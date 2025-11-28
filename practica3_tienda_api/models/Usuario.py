from uuid import uuid4

class Usuario:
    """
    Representa a cualquier persona que interactúe con la tienda.
    id: identificador único (string) generado automáticamente
    nombre del usuario
    email: correo electrónico
    """
    def __init__(self, nombre: str, email: str, id_: str | None = None) -> None:
        nombre = (nombre or "").strip()
        email = (email or "").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not email:
            raise ValueError("El email no puede estar vacío.")
        self.id: str = id_ or str(uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:  #Por defecto, un usuario no es admin
        return False

    def __str__(self) -> str:
        rol = "Administrador" if self.is_admin() else "Cliente"
        return f"[{self.id}] {self.nombre} <{self.email}> ({rol})"


class Cliente(Usuario):  #Usuario cliente de la tienda, con dirección
    def __init__(self, nombre: str, email: str, direccion: str, id_: str | None = None) -> None:
        super().__init__(nombre, email, id_)
        direccion = (direccion or "").strip()
        if not direccion:
            raise ValueError("La dirección no puede estar vacía.")
        self.direccion: str = direccion

    def __str__(self) -> str:
        return f"{super().__str__()} | dirección: {self.direccion}"


class Administrador(Usuario):  #Usuario administrador de la tienda
    def is_admin(self) -> bool:
        return True