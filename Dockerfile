# 1. Imagen base
FROM python:3.12-slim

# 2. Configuración básica de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos solo requirements primero (mejor cache)
COPY requirements.txt .

# 5. Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el resto del código del proyecto
COPY . .

# 7. Creamos usuario no root y damos permisos
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 8. Comando de inicio
CMD ["python", "src/main.py"]