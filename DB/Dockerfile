# Usa la imagen oficial de PostgreSQL como base
FROM postgres:latest

# Establece la contraseña de PostgreSQL
ENV POSTGRES_PASSWORD=123

# Expone el puerto 8484 para acceder desde la máquina local
EXPOSE 5432

# ojooooooooo modifica esto para que apunte a una carpeta existente en tu máquina local
VOLUME /~/cochinolandia:/var/lib/postgresql/data

# Inicializa la base de datos y crea una base de datos llamada "prueba"
COPY init.sql /docker-entrypoint-initdb.d/

# Define la base de datos que se creará automáticamente al iniciar el contenedor
ENV POSTGRES_DB=coda
