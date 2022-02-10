# Houmer Markers

Solución al desafío planteado por Houm, para obtener métricas sobre sus Houmers

## Consideraciones




## Ejecución en ambiente local

Para ejecución de los servicios en ambiente local para **desarrollo**, hacer:


0.- Clonar proyecto

```
git clone https://github.com/felipesanma/houmer-markers.git
```

1.- Entrar al directorio "houmer-markers". Levantar mysql y rabbitmq:

```
docker-compose -f extra-utils.yml up
```

Se encontrará operativo cuando se vean las siguientes líneas:

```
database_1  | 2022-02-10T20:35:25.841618Z 0 [Note] mysqld: ready for connections.
rabbitmq_1  | Server startup complete; 6 plugins started.

```
2.- Esperar a que se levante correctamente lo del paso 1. Luego, ejecutar:

```
docker-compose up
```

Se encontrará operativo cuando se vea lo siguiente:
```
houmerapi_1 | INFO: Application startup complete.
```

## Documentación

Una vez levantado, dirigirse a: http://localhost:8080/redoc

Se encontrará toda la documentación asociado al consumo de los servicios REST.

## Test Data

Para la inyección de datos con localizaciones de propiedades, revisar el siguiente jupyter notebook https://github.com/felipesanma/houmer-markers/blob/master/data/Get%20Properties%20Data%20-%20Houm_Challenge.ipynb


## To do

1. Configuración de log files.
2. Documentación para uso en producción (con ECS, bajo un pipeline en gitlab).
3. Test del código.
4. Generación de data para houmers de forma random.
