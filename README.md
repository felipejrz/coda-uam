## README.md

**# Requisitos**

* Docker y Docker Desktop

**# Creación de archivo de variables**

1. En el directorio `coda-src/ssocial` Crea un archivo llamado `env_vars.py`.
2. Copia y pega el siguiente código en el archivo:

```python
import os

os.environ.setdefault('DJANGO_SECRET_KEY', '<key>')
os.environ.setdefault('RDS_DB_NAME', 'coda')
os.environ.setdefault('RDS_USERNAME', 'postgres')
os.environ.setdefault('RDS_PASSWORD', '<contraseña>')
os.environ.setdefault('RDS_HOSTNAME', 'margarito-contenedor')
os.environ.setdefault('RDS_PORT', '5432')
os.environ.setdefault('DJANGO_DEBUG', 'True')
os.environ.setdefault('TUTORIAS_DOMINIO', '<dominio>')
os.environ.setdefault('IP_COMPUTADORA', 'localhost')
os.environ.setdefault('EMAIL_HOST_PASSWORD', '<email>')
```

3. Reemplaza los valores entre `< >` con la información correspondiente.

**# Creación de la base de datos**

1. Cambia al directorio `DB`.
2. Modifica las líneas 5 y 10 del archivo `Dockerfile` para que coincidan con tu configuración.
3. Ejecuta los siguientes comandos:

```
docker network create <nombre-red>
docker build -t margarito .
docker run -d --network <nombre-red> -p 5432:5432 --name margarito-contenedor margarito
docker exec -it margarito-contenedor psql -U postgres -c 'CREATE DATABASE coda;'
```

**# Creación del servidor Django**

1. Cambia al directorio `coda-src`.
2. Ejecuta el siguiente comando:

```
docker build -t djangarito .
```

3. Inicia el servidor Django:

```
docker run -d --network <nombre-red> -p 8000:8000 --name djangarito_contenedor djangarito
```

**# Implementación del servidor**

1. En Docker Desktop, selecciona la pestaña "Contenedores".
2. Busca y selecciona el contenedor `djangarito_contenedor`.
3. Selecciona la pestaña "Exec".
4. Ejecuta los siguientes comandos:

```
python3 manage.py migrate
python3 manage.py createsuperuser
```

**# Notas adicionales**

* Asegúrate de reemplazar los valores predeterminados en el archivo `env_vars.py` con la información de tu proyecto.
* Puedes cambiar el nombre de la red y los nombres de los contenedores según tus preferencias.
* Para obtener más información sobre cómo usar Docker y Django, consulta la documentación oficial:
    * [https://docs.docker.com/](https://docs.docker.com/)
    * [https://docs.djangoproject.com/](https://docs.djangoproject.com/)

## Suerte ingrato