from fastapi import FastAPI
from Services.Tienda_service import TiendaService

# Crear la app de FastAPI
app = FastAPI(
    title="Tienda Online - Práctica 3",
    version="1.0.0",
)

# Instancia global de la lógica de negocio
tienda = TiendaService()


@app.get("/")
def root():
    """Endpoint sencillo para comprobar que la API funciona."""
    return {"mensaje": "API de la tienda online funcionando"}