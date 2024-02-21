# Usa la imagen base de Python para Django
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al directorio de trabajo del contenedor
COPY . .

# Ejecuta makemigrations durante la construcción de la imagen
RUN python manage.py makemigrations

# Expone el puerto 8000 para acceder a la aplicación Django
EXPOSE 8000

# Comando predeterminado para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
