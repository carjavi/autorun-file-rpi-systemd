<p align="center"><img src="./img/bashlogo.png" width="500"  alt=" " /></p>
<h1 align="center">Run a program on your Raspberry Pi at Startup with Daemon Service SYSTEMD</h1> 
<h4 align="right">Aug 24</h4>

<img src="https://img.shields.io/badge/Hardware-Raspberry%20ver%204-red">
<img src="https://img.shields.io/badge/Hardware-Raspberry%203B%2B-red">
<img src="https://img.shields.io/badge/Hardware-Raspberry%20Zero-red">

<br>

Este script permite crear de forma interactiva un servicio que se iniciara cada vez que se inicie la raspberry. Puede correr un archivo en Python, NodeJS o Bash. Para crear el servicio debemos tener presente:

1. Definir un nombre para el servicio.
2. Definir con que programa vamos abrir la aplicación (python3, node o bash).
3. Tener la ruta del archivo a ejecutar (ejemplo: /home/carjavi/hello-world.py).


<br>

```create-autorun-service.sh```
```bash 
#!/usr/bin/env bash

# Define colors
readonly ANSI_RED="\033[0;31m"
readonly ANSI_GREEN="\033[0;32m"
readonly ANSI_YELLOW="\033[0;33m"
readonly ANSI_RASPBERRY="\033[0;35m"
readonly ANSI_ERROR="\033[1;37;41m"
readonly ANSI_RESET="\033[m"
readonly RASPAP_LATEST="2.0"

# Outputs a welcome message
function display_welcome() {
echo -e "${ANSI_RASPBERRY}\n"
echo -e "                            d8b                   d8b" 
echo -e "                            Y8P                   Y8P"
echo -e "                                                     "
echo -e " .d8888b  8888b.  888d888  8888  8888b.  888  888 888"
echo -e "d88P'        '88b 888P'    '888     '88b 888  888 888" 
echo -e "888      .d888888 888       888 .d888888 Y88  88P 888" 
echo -e "Y88b.    888  888 888       888 888  888  Y8bd8P  888" 
echo -e " 'Y8888P 'Y888888 888       888 'Y888888   Y88P   888" 
echo -e "                            888                      " 
echo -e "                           d88P                      " 
echo -e "                         888P'                       " 
echo -e "                                                     "
echo -e "${ANSI_GREEN}"
echo -e "The Quick Installer will guide you through a few easy steps${ANSI_RESET}"
echo -e "\033[1;32m***************************************************************$*\033[m"
echo -e "\n\n"
}

# calling Titulo 
display_welcome
    
#sleep 3seg
sleep 3

# Comprobando si el script se está ejecutando con privilegios de superusuario
if [ "$EUID" -ne 0 ]; then 
  echo "Por favor, ejecuta este script como root o utilizando sudo. ej: sudo ./create-autorun-service.sh --verbose."
  exit 1
fi

# Solicitar nombre del servicio
read -p "Ingresa el nombre del servicio: " SERVICE_NAME

# Path del archivo a correr
read -p "Path del archivo a correr (ejemplo: /home/carjavi/): " FILE_PATH

# Solicitar comando ExecStart
read -p "Ingresa con que aplication se va a correr el serivicio (python3 -u/node/bash): " EXEC_START

# Nombre del archivo a correr
read -p "Nombre del archivo a correr (ejemplo: hello-world.py): " NAME_FILE

echo
echo "------------------------------"
echo "Creating the service file..."
echo "------------------------------"
echo

# Contenido del archivo .service
SERVICE_CONTENT="[Unit]
Description=$SERVICE_NAME
After=network.target

[Service]
ExecStart=/bin/bash -c 'cd $FILE_PATH && $EXEC_START $NAME_FILE >> $FILE_PATH$SERVICE_NAME.log'
Restart=on-failure

[Install]
WantedBy=multi-user.target"

# Ruta al archivo .service
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME.service"

# Creando el archivo .service
echo "$SERVICE_CONTENT" > $SERVICE_PATH

echo
echo "-------------------------------------"
echo "$SERVICE_NAME Service created successfully."
echo "-------------------------------------"
echo

# permission (Propietario: Puede leer y escribir el archivo /Grupo y otros solo lectura)
chmod 644 /etc/systemd/system/$SERVICE_NAME.service

# Start deamon code
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

echo
echo "-------------------------------------"
echo "$SERVICE_NAME Service started successfully."
echo "-------------------------------------"
echo

# Delete installer
#create-autorun-service.sh

echo
echo "-------------------------------------"
echo "Ready. System will reboot in 10 seconds..."
echo "-------------------------------------"
echo

sleep 10 && reboot
```

<br>

> :warning: **Warning:** Para correr el archivo hay que darle permiso de ejecución:
```bash 
sudo chmod +x create-autorun-service.sh
```

## Run Script
```bash 
sudo ./create-autorun-service.sh --verbose
```

> :bulb: **Tip:** Si deseamos correr un archivo Python3, conviene usar la opción ```-u``` ya que ayuda a ver los valores de salida en tiempo real si usamos ```journalctl```.
> 
> Se creará un archivo con el mismo nombre del servicio pero ```.log``` que registrará todas las salidas (stout) print/console del archivo que esta correindo. La salida no sobre-escribirá el archivo sino que agregará sin sobreescribirlo
<br>

# Daemon Service SYSTEMD commands (summary)
```bash 
sudo systemctl daemon-reload # Recarga su configuración. Esto es necesario después de hacer cambios en los archivos de configuración de unidades
sudo systemctl status SERVICE_NAME
sudo systemctl stop SERVICE_NAME
sudo systemctl start SERVICE_NAME
sudo systemctl disable SERVICE_NAME
sudo systemctl enable SERVICE_NAME
sudo systemctl restart SERVICE_NAME
systemctl --failed  #ver los servicios que fallaron
systemctl list-unit-files --type=service --state=enabled # Ver todos los servicios que inician automáticamente al arrancar el sistema

```
# Edit Service
> :warning: **Warning:** ```sudo systemctl daemon-reload```deberá ingresar este  comando cada vez que cambie su archivo .service,ya que systemd necesita saber que se ha actualizado.
```bash 
sudo nano /etc/systemd/system/SERVICE_NAME
```


# Debugging
La salida de systemd (por ejemplo, sentencias print() o mensajes de error) es capturada por el sistema journalctl y se puede ver con el siguiente comando:
```bash 
sudo journalctl -f -u SERVICE_NAME
```
Esto puede dar una idea de lo que está pasando con su servicio o programa.

# Delete service
```bash 
sudo rm /lib/systemd/system/SERVICE_NAME.service
sudo systemctl daemon-reload
sudo reboot
```
<br>

# Considerations
## Ejecutar directamente la aplicación desde el Daemon Service SYSTEMD
ejemplo:
```bash 
ExecStart=/usr/bin/python /path-to-your-python-project/python_file.py
```

```La forma más sencilla de ejecutar un script de Python, pero no se recomienda en la mayoría de los casos.``` El  no proporcionar la ruta correcta de Pythono y Nodejs traerá problema para reconocer los módulos y librerías necesarios para correr la aplicación. 

<br>

## Ejecutar Python o NodeJS dentro de la carpeta donde esta la aplicación en el Daemon Service SYSTEMD
ejemplo:
```bash 
ExecStart=/bin/bash -c 'cd /home/ubuntu/project/ && python app.py'
```
```Esta sería la mejor forma de correr una aplicación.``` Es mejor ir a la carpeta correspondiente y ejecutar scripts de Python o NodeJS allí. Te relajas con respecto a las rutas de carpetas que no coinciden. Ahora estamos usando bash para ejecutar varios scripts.

El comando ```bash -c``` se utiliza para ejecutar una cadena de comandos de Bash directamente desde la línea de comandos. ```-c``` Indica que lo que sigue es una cadena de comandos a ejecutar. separados por ```;```, ```&&```, o ```||```, dependiendo de cómo quieras encadenar la ejecución. ejemplo:
```bash 
bash -c "comando1; comando2; comando3"
```

<br>

## Ejecutar la aplicación con su entorno en el Daemon Service SYSTEMD
ejemplo python virtual environment (entorno virtual de Python):
```bash 
ExecStart=/bin/bash -c 'cd /home/ubuntu/project/ && source env/bin/activate && python app.py'
```
Esta es otra forma recomendada. Después de eso, puedes agregar tantos comandos como quieras

<br>

<br>

# Another method to run a program when starting the raspberry

## (rc.local)
This is especially useful if you want to power up your Pi without a connected monitor, and have it run a program without configuration or a manual start.

1. permiso de ejecución al archivo
  ```bash 
  $ sudo chmod +x fichero.py
  ```
2. sudo nano /etc/rc.local

```bash 
...
python3 /home/pi/fichero.py
/usr/bin/python3 /home/pi/example.py
node /home/pi/fichero.js
sudo bash /home/pi/di_update/Raspbian_For_Robots/upd_script/rc.sh

exit 0
```
 > :memo: **Note:** Si programa debe devolver el control al script o la Raspberry Pi nunca podrá terminar de arrancar. Si su programa realiza un bucle infinito, debe ejecutarlo en segundo plano agregando un & después de ordenar. En nuestro caso esto daría:
```bash 
/usr/bin/python3 /home/pi/example.py &
```
<br>

## .bashrc
rc.local es un buen lugar para iniciar su programa cada vez que se inicia el sistema (antes de que los usuarios puedan iniciar sesión o interactuar con el sistema). Si desea que su programa se inicie cada vez que un usuario inicie sesión o abra una nueva terminal, considere agregar una línea similar a /home/pi/.bashrc.
```bash 
sudo nano /home/pi/.bashrc
```
Go to the last line of the script and add:

```bash 
echo Running at boot 
sudo python /home/pi/sample.py
sudo reboot
```
<br>

# Troubleshooting rc.local & .bashrc
Estos métodos de arranque automáticos pueden dar problemas si la ruta de la aplicación no esta bien definida, los módulos y librerías que utiliza dicha operación dará problemas. Una solución es agregar la ruta de la aplicación antes de correr el programa. Ejemplo en Python:

1. Desde el terminal correr: python3
   ```
   >>import sys
   >>sys.path
   ```
2. El Output sera algo como:
   ```
   ['/usr/lib/python39.zip', '/usr/lib/python3.9', '/usr/lib/python3.9/lib-dynload', '/home/carjavi/.local/lib/python3.9/site-packages', '/usr/local/lib/python3.9/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.9/dist-packages']
   ```
3. con esta data se debe generar un String de este tipo
   ```
   export PATH="$PATH:/usr/lib/python39.zip:/usr/lib/python3.9:/usr/lib/python3.9/lib-dynload:/home/maquintel/.local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/lib/python3/dist-packages:/usr/lib/python3.9/dist-packages"
   ```
4. Este string debe antes de ejecutar el comando de arranque del archivo en ```rc.local``` ó ```.bashrc```. ejemplo:
   ```
   export PATH="$PATH:/usr/lib/python39.zip:/usr/lib/python3.9:/usr/lib/python3.9/lib-dynload:/home/maquintel/.local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/lib/python3/dist-packages:/usr/lib/python3.9/dist-packages"

   sudo python3 /home/carjavi/sample.py
   ```

<br>

more info: https://github.com/carjavi/raspberry-pi-guide?tab=readme-ov-file#daemon-service-systemd

<br>

---
Copyright &copy; 2022 [carjavi](https://github.com/carjavi). <br>
```www.instintodigital.net``` <br>
carjavi@hotmail.com <br>
<p align="center">
    <a href="https://instintodigital.net/" target="_blank"><img src="./img/developer.png" height="100" alt="www.instintodigital.net"></a>
</p>

