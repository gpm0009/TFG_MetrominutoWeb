# Metrominuto_TFG
## Trabajo de fin de grado

### Autor
- Guillermo Paredes Muga

### Tutores
- Dr. Álvar Arnaiz González
- Dr. César Ignacio García Osorio

### Resumen
La sociedad actual en la que vivimos inmersos, donde la prisa y
la inmediatez dominan nuestro día a día, los desplazamientos a pie
siempre quedan en segundo lugar. Esto, en parte, también se debe
a que actualmente las áreas urbanas cuentan con muy pocas zonas
peatonales, ya que la estructura de las mismas no está pensado para
ello.

Es por ello que era de urgente necesidad que surgieran planes
o ideas dedicados a solventar este problema, y fomentar dentro de
las áreas urbanas los desplazamientos a pie. Esto puede trasladarse
no solo a los propios vecinos de dichas áreas, si no que también al
turismo.

Como solución a estos problemas aparece Metrominuto, un mapa
sinóptico que representa trayectos entre varios puntos, junto con
los tiempos de desplazamiento entre dichos puntos. Este proyecto
busca la creación automática mediante una aplicación web de estos
metrominutos, de manera que sea el proprio usuario quien elija y
personalice su propio mapa.

### Página Web
http://metrominutoweb.azurewebsites.net/


### Vídeo de presentación y demostración de la aplicación.
https://www.youtube.com/watch?v=JMNwoWID_xU


### Funcionalidades
- Generación automática de metrominutos.
- Selección de diferentes puntos en un mapa.
- Visualización de dichos puntos con la información de la distancia existente entre ellos. 
- Libertad del usuario para añadir, eliminar o modificar dichos puntos.

### Instalación y configuración
#### Instalar python
Debemos tener instalado Python en nuestro sistema. Para ello visitar [Python Download](https://www.python.org/downloads/)

#### Clonar el repositorio
`git clone https://github.com/gpm0009/TFG_MetrominutoWeb`

#### Configuración
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
##### Firebase
Incluye en la parte inferior del fichero widget.html tu ```clientId``` de Google.
Sustituye en el fichero ```Metrominuto\metrominuto_app\static\js\firebase-config.js``` tus credenciales de [Firebase](https://console.firebase.google.com/).
