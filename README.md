# Tienda DevOps

Autor: Pablo Barrán

Aplicación Python que implementa una tienda online.
Las clases de dominio están en la carpeta `models`, los servicios en `Services`
y el archivo `main.py` ejecuta algunos casos de prueba usando `TiendaService`
(registro de usuarios, alta de productos y simulación de compras).

## Docker

### Construir la imagen

```bash
docker build -t pablobafa/tienda-service:1.0.0 .