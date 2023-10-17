# Curso Data Engineering Coderhouse - Proyecto de Benjamín Luengo Ackermann
**Proyecto desarollado a lo largo del curso Data Engineering brindado por la academia Coderhouse.**

    Para este proyecto se eligió una API de acceso público y gratuito (sin auth) que devuelve los datos de la cotización al final del dia de mas de 150 de las principales criptomonedas del mercado.
    De esta manera obtenemos un JSON con el nombre de la criptomoneda (e.g: BTC) y su cotización equivalente a un dolar, es decir cuanto vale 1 USD en esa criptomoneda. 
    Adicionalmente, se calcula el valor de una unidad de la criptomoneda (e.g: 1 BTC) y su equivalencia en dólares.

    La intención es almacenar día a día los valores de la cotización y así lograr una línea histórica para cada criptomoneda.

    Se puede pensar este script como uno que se corre diariamente dentro de una organización a fin de obtener las cotizaciones y almacenarlas con el objetivo de lograr consultas que agreguen valor a la compañia en una linea  temporal histórica desde el primer día de puesta en marcha del script hasta la actualidad.


### :globe_with_meridians: Repositorio API: https://github.com/fawazahmed0/currency-api#readme


### :floppy_disk: Base de Datos
A nivel de persistencia teniendo en cuenta que en una BD Relacional la tabla tendria por columnas:
>
> - nombre *(unique) (varchar(256))*
> - fecha *(date)*
> - precio_unitario *(decimal(38, 10))* [^1]
> - precio_relativo *(numeric(38, 10))* [^2]  
 
 En base a estas columnas y recordando que una BD Columnar consiste en pivotear la tabla relacional se obtendrán como filas el nombre, fecha, precio_unitario y precio_relativo

[^1]: Cuanto vale en dólares una unidad de la criptomoneda **(e.g: 1 BTC = 26010 USD)**
[^2]: Cuanto vale en la criptomoneda correspondiente una unidad de dolar **(e.g: 1 USD = 0.00003845 BTC)** 


### :golfing: ¿Como correr el container?
Para correr el container, en primer lugar, debemos tener instalado:

> - *Docker*
> - *Docker-compose*

Partiendo de esa base, se deben seguir los siguientes pasos para correr el programa:

1. Descargar en modo comprimido o clonar el repositorio
2. Abrir una terminal dentro del proyecto (*Data-Engineering-Coderhouse*)
3. En la terminal, usar el comando ```docker-compose up airflow-init```
4. Ejecutar el comando ```docker-compose up```. Esto levantará el cliente web de Airflow donde podremos ver la ejecución de la tarea
5. Dentro del navegador ir al [localhost](http://localhost:8080) e introducir las siguientes credenciales:
    - *Username:* Benjamin
    - *Password*: Luengo
6. Ya en el cliente de Airflow se puede ver que el DAG estará listado y corriendo una vez por día


### :incoming_envelope: Envío de Alertas
El envío de alertas se puede modificar cambiando los valores de treshold presentes en la función ```get_tresholds_for_top_10_crypto``` del *[Módulo Alertas](plugins/alertas.py)*. 
Estas alertas corresponden a las criptomonedas elegidas arbitrariamente en los pasos anteriores y serán enviadas a los correos especificados como variables de entorno en el archivo *[docker-dompose](docker-compose.yaml)*.

