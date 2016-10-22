# CornerShop Todo - REST API
[![Build Status](https://travis-ci.org/royarzun/cornershopTodo.svg?branch=develop)](https://travis-ci.org/royarzun/cornershopTodo)

## Introduccion

El desafio era desarrollar una API capaz de manejar una ***TODO list***, que cubriera los siguientes requerimientos:

- Registrar un usuario.
- Agregar tareas al TODO list.
- Marcar una tarea como resuelta.
- Obtener la lista de tareas y su estado actual.

Como medio de autentificacion se usa DRF [TokenAuthentication](http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)

## Instalacion

requerimientos del sistema

```sh
Django==1.9
djangorestframework==3.3.0
django-rest-swagger==0.3.10
```

Primero, instalar las dependencias para la aplicacion

```sh
$ pip install -r requirements.txt
```

Despues de instalada las dependencias ya puedes correr el development server

```sh
$ ./manage.py runserver
```

## Usando la API

Para ver la documentacion completa de la API en la interfaz de [Swagger](http://swagger.io/), puede referirse a la URL:

```sh
$ http://localhost:8000/docs
```

En esta interfaz podra leer la documentacion e interactuar directamente con los endpoints

## Consideraciones

- Teniendo en mente que las tareas se pueden modificar despues de creadas, se permite crear tareas vacias
- Usuario solo modifica sus tareas

## Licencia

    Copyright 2016 Ricardo Oyarzun

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
