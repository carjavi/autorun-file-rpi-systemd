#!/usr/bin/env bash

# Solicita el nombre del archivo a correr
read -p "Nombre del archivo a correr (ejemplo: hello-world.py): " NAME_FILE

# Elimina la extensión del archivo usando 'basename'
NAME_NO_EXTENSION="${NAME_FILE%.*}"

# Muestra el nombre del archivo sin la extensión
echo "El nombre del archivo sin la extensión es: $NAME_NO_EXTENSION"