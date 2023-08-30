# Curso Data Engineering Coderhouse - Proyecto de Benjamín Luengo Ackermann
Proyecto desarollado a lo largo del curso Data Engineering brindado por la academia Coderhouse.

    Para este proyecto se eligió una API de acceso público y gratuito (sin auth) que devuelve los datos de la cotización al final del dia de mas de 150 de las principales criptomonedas del mercado.
    De esta manera obtenemos un JSON con el nombre de la criptomoneda (e.g: BTC) y su cotización equivalente a un dolar, es decir cuanto vale 1 USD en esa criptomoneda. 
    Adicionalmente, se calcula el valor de una unidad de la criptomoneda (e.g: 1 BTC) y su equivalencia en dólares.

    La intención es almacenar día a día los valores de la cotización y así lograr una línea histórica para cada criptomoneda.

    Se puede pensar este script como uno que se corre diariamente dentro de una organización a fin de obtener las cotizaciones y almacenarlas con el objetivo de lograr consultas que agreguen valor a la compañia en una linea  temporal histórica desde el primer día de puesta en marcha del script hasta la actualidad.

 Repositorio API: https://github.com/fawazahmed0/currency-api#readme