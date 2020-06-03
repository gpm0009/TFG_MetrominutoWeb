# Metrominuto_TFG
## Trabajo de fin de grado

### Autor
- Guillermo Paredes Muga

### Tutores
- Dr. Álvar Arnaiz González
- Dr. César Ignacio García Osorio

### Funcionalidades
- Generación automática de metrominutos.
- Selección de diferentes puntos en un mapa.
- Visualización de dichos puntos con la información de la distancia existente entre ellos.
- Calculo del trayecto más corto entre ellos. 
- Libertad del usuario para añadir, eliminar o modificar dichos puntos.

### Instalación y configuración
Debemos tener instalado Python en nuestro sistema. Para ello visitar [Python Download](https://www.python.org/downloads/)

Una vez tengamos Python instalado, debemos decargar el proyecto:
`git clone https://github.com/gpm0009/TFG_MetrominutoWeb`

Para la confuguración del entorno de trabajo, en entre proyecto se explicará como configurarlo en [PyCharm](https://www.jetbrains.com/pycharm/download), pero para su configuración en Visual Studio Code puede seguir esta [guía](https://code.visualstudio.com/docs/python/tutorial-flask).

Desde PyCharm, abre el directorio del proyecto, y crea un nuevo entorno virtual. Posteriormente selecciónalo como interprete del proyecto. 
```
Files - Settings - Project Interpreter - Add - Virtual Envirorment - New
```

A continuación, instala las dependencias del proyecto ejecutando en la consola:
`pip -r install requirements .txt`

Para obtener una API_KEY de Google puedes hacerlo desde la propia página de [documentación](https://developers.google.com/maps/documentation/javascript/get-api-key?hl=es) de Google. 

Configura las variables de entorno:
```
GOOGLE_API_KEY
SECRET_KEY
ENVIRORMENT
```
