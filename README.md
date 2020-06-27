# Invest Simulator

## Heroku Demo

The demo can be found using [this link](https://invest-simulator-23.herokuapp.com/).
Test User:

- **username**: test-user 
- **password**: wuqgoj-hibgix-7Bysza

Aplicación web orientada al público general que simula inversiones en tiempo real.

# Integrantes:

- Rodrigo Lucero
- Agustin Gomez
- Igor Andruskiewitsch
- Marco Martinelli
- Federico Rivero
- Alexis Guerra

# Instalacion:
Requisitos previos:
- Homebrew.
- Git.
- Python 3.6/3.7.

Se deben seguir los siguientes pasos, ejecutando cada comando en la terminal:
#### 1. Clonar repositorio de la aplicacion:
```
mkdir investsimulator
cd investsimulator
git clone https://gitlab.com/LocosXelAsado/investsimulator.git
```
#### 2. Instalar virtualenv:
En linux: 
```
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
```
En MacOS:
```
brew install python
pip3 install virtualenv
```
#### 3. Crear entorno virtual:
```
virtualenv venv
```
#### 4. Activar entorno virtual:
```
source ./venv/bin/activate
```
#### 5. Instalar requerimientos:
```
pip3 install -r investsimulator/requirements.txt
```
Esto instalara los siguientes paquetes:
-	dj-config-url
-	Django==2.1.2
-	django-common-helpers==0.9.2
-	django-cron==0.5.1
-	django-crontab==0.7.1
-	gunicorn==19.9.0
-	idna==2.7
-	ipython==7.0.1
-	ipython-genutils==0.2.0
-	jedi==0.13.1
-	kombu==4.2.1
-	mock==2.0.0
-	parso==0.3.1
-	pbr==4.3.0
-	pep8==1.7.1
-	pexpect==4.6.0
-	pickleshare==0.7.5
-	Pillow==5.3.0
-	prompt-toolkit==2.0.5
-	psycopg2==2.7.6.1
-	ptyprocess==0.6.0
-	Pygments==2.2.0
-	python-dateutil==2.7.5
-	pytz==2018.5
-	requests==2.19.1
-	simplegeneric==0.8.1
-	six==1.11.0
-	traitlets==4.3.2
-	urllib3==1.23
-	vine==1.1.4
-	wcwidth==0.1.7
-	whitenoise==4.1.1
-	psycopg2==2.7.6.1

#### 7. Hacer migraciones:
```
python3 investsimulator/manage.py migrate
```
#### 8. Correr el servidor: 
```
python3 investsimulator/run.py
```
Esto es debido a que el servidor corre como un proceso hijo de un proceso que se encarga de buscar prestamos que hayan expirado, a los fines de tomar las acciones correspondientes sobre estos.
#### 9. Abrir la aplicacion:
En el navegador deseado, ingresar la url:
```
localhost:8000
```
