
![Wini, mascota oficial del proyecto de servicio social](/static/img/wini_el_pato.png)

# Instrucciones de ejecución

Estas son las instrucciones para ejecutar el proyecto utilizando Docker.

## Requisitos

Asegúrate de tener Docker instalado en tu sistema antes de continuar. Puedes descargar e instalar Docker desde [Docker's official website](https://www.docker.com/get-started).

## Pasos para ejecutar el proyecto

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/mautx/servicio_social.git
   ```

 
    Reemplaza tu_usuario con tu nombre de usuario de GitHub.

    Navega al directorio del proyecto:
 
    

   ```bash
cd servicio_social
```
Construye la imagen Docker utilizando el Dockerfile proporcionado:

bash

docker build -t margarito .

Esto construirá la imagen Docker con el nombre margarito.

Ejecuta un contenedor basado en la imagen recién creada:

bash

    docker run -d -p <tu_puerto>:5432 --name margarito-contenedor margarito

    Reemplaza <tu_puerto> con el puerto que deseas usar en tu máquina local para acceder a PostgreSQL dentro del contenedor.

    ¡Listo! Ahora tu contenedor de PostgreSQL está en funcionamiento. Puedes acceder a él utilizando cualquier cliente de PostgreSQL apuntando a localhost:<tu_puerto>.

Si deseas detener y eliminar el contenedor en algún momento, puedes hacerlo ejecutando los siguientes comandos:

bash

docker stop margarito-contenedor
docker rm margarito-contenedor

Esto detendrá y eliminará el contenedor. Ten en cuenta que si deseas volver a ejecutar el contenedor más tarde, deberás crearlo nuevamente utilizando el comando docker run.