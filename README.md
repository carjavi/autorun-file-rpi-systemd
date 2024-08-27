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

```file: create-autorun-service.sh```
```
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

# Solicitar comando ExecStart
read -p "Ingresa con que aplication se va a correr el serivicio (python3/node/bash): " EXEC_START

# Path y nombre del archivo a correr
read -p "Nombre del archivo a correr (ejemplo: /home/carjavi/hello-world.py): " FILE_PATH

echo
echo "------------------------------"
echo "Install and Start Services..."
echo "------------------------------"
echo

# Contenido del archivo .service
SERVICE_CONTENT="[Unit]
Description=$SERVICE_NAME
After=network.target

[Service]
ExecStart=/usr/bin/$EXEC_START $FILE_PATH
Restart=on-failure

[Install]
WantedBy=multi-user.target"

# Ruta al archivo .service
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME.service"

# Creando el archivo .service
echo "$SERVICE_CONTENT" > $SERVICE_PATH

echo
echo "-------------------------------------"
echo "Service $SERVICE_NAME created and started successfully."
echo "-------------------------------------"
echo

# Start deamon code
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

# Delete installer
#create-autorun-service.sh

echo
echo "-------------------------------------"
echo "Service $SERVICE_NAME created and started successfully."
echo "-------------------------------------"
echo

echo
echo "-------------------------------------"
echo "Ready. System will reboot in 10 seconds..."
echo "-------------------------------------"
echo

sleep 10 && reboot
```

<br>

> :warning: **Warning:** Para correr el archivo hay que darle permiso de ejecución:
```
sudo chmod +x create-autorun-service.sh
```

<br>

# Daemon Service SYSTEMD commands (summary)
```
sudo systemctl daemon-reload
sudo systemctl status SERVICE_NAME
sudo systemctl stop SERVICE_NAME
sudo systemctl start SERVICE_NAME
sudo systemctl disable SERVICE_NAME
sudo systemctl enable SERVICE_NAME
sudo systemctl restart SERVICE_NAME
```
# Edit Service
> :warning: **Warning:** ```sudo systemctl daemon-reload```deberá ingresar este  comando cada vez que cambie su archivo .service,ya que systemd necesita saber que se ha actualizado.
```
sudo nano /etc/systemd/system/SERVICE_NAME
```

# Debugging
La salida de systemd (por ejemplo, sentencias print() o mensajes de error) es capturada por el sistema journalctl y se puede ver con el siguiente comando:
```
sudo journalctl -f -u SERVICE_NAME
```
Esto puede dar una idea de lo que está pasando con su servicio o programa.

# Delete service
```
sudo rm /lib/systemd/system/clock.service
sudo systemctl daemon-reload
sudo reboot
```


more info: https://github.com/carjavi/raspberry-pi-guide?tab=readme-ov-file#daemon-service-systemd

<br>

---
Copyright &copy; 2022 [carjavi](https://github.com/carjavi). <br>
```www.instintodigital.net``` <br>
carjavi@hotmail.com <br>
<p align="center">
    <a href="https://instintodigital.net/" target="_blank"><img src="./img/developer.png" height="100" alt="www.instintodigital.net"></a>
</p>

