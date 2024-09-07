import time

def leer_temperatura():
    # Abre el archivo que contiene la temperatura de la CPU
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as archivo:
        # Lee el valor en miligrados Celsius y conviértelo a grados Celsius
        temp_miligrados = int(archivo.read())
        temperatura_celsius = temp_miligrados / 1000.0
    return temperatura_celsius

def main():
    while True:
        temperatura = leer_temperatura()
        print(f"Temperatura del procesador: {temperatura:.2f}°C")
        time.sleep(2)  # Espera 2 segundos antes de la próxima lectura

if __name__ == "__main__":
    main()
