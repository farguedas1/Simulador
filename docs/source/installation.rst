===========
Instalación
===========

Requisitos
==========
La aplicación esta escrita en Python y puede correr en cualquier sistema operativo
que lo soporte, siempre y cuando se tengan instaladas las siguientes herramientas:

- git
- python 3.5+
- pip

Instalación
===========
Para instalar la aplicación es necesario descargarla el código fuente desde
GitHub en https://github.com/farguedas1/Simulador.git

Una vez que se ha descargado el código, es necesario instalar las dependencias
usando la herramienta ``pip``:

.. code::

  pip install -r requirements.txt

Iniciar la aplicación
=====================
Para correr la aplicación utilizar el siguiente comando desde la raíz del
código fuente:

.. code::

  python3 -m bokeh serve --show app

Este comando procedera a abrir un navegador apuntando hacia la aplicación:

.. image:: screenshot.jpeg
