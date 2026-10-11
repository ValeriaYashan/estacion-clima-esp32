#!/usr/bin/env python3
"""Lee las lineas CSV que imprime el ESP32 por serial y las guarda con fecha y hora.

Uso:
    python software/registrar.py --puerto COM3
    python software/registrar.py --puerto /dev/ttyUSB0 --salida datos/lecturas.csv
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

CABECERA = ["fecha_hora", "temperatura_c", "humedad_pct"]


def parsear_linea(linea):
    """Convierte 'tiempo_ms,temp,hum' en (temp, hum). Devuelve None si no es una lectura."""
    linea = linea.strip()
    if not linea or linea.startswith("#") or linea.startswith("tiempo_ms"):
        return None
    partes = linea.split(",")
    if len(partes) != 3:
        return None
    try:
        temperatura = float(partes[1])
        humedad = float(partes[2])
    except ValueError:
        return None
    if not (-40.0 <= temperatura <= 80.0 and 0.0 <= humedad <= 100.0):
        return None
    return temperatura, humedad


def abrir_csv(ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not ruta.exists() or ruta.stat().st_size == 0
    archivo = ruta.open("a", newline="", encoding="utf-8")
    escritor = csv.writer(archivo)
    if nuevo:
        escritor.writerow(CABECERA)
        archivo.flush()
    return archivo, escritor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--puerto", required=True, help="Puerto serie (COM3, /dev/ttyUSB0, ...)")
    parser.add_argument("--baudios", type=int, default=115200)
    parser.add_argument("--salida", default="datos/lecturas.csv")
    args = parser.parse_args()

    try:
        import serial
    except ImportError:
        sys.exit("Falta pyserial: pip install -r software/requirements.txt")

    archivo, escritor = abrir_csv(args.salida)
    print(f"Registrando en {args.salida}. Ctrl+C para detener.")
    try:
        with serial.Serial(args.puerto, args.baudios, timeout=5) as puerto:
            while True:
                linea = puerto.readline().decode("utf-8", errors="ignore")
                lectura = parsear_linea(linea)
                if lectura is None:
                    continue
                marca = datetime.now().isoformat(timespec="seconds")
                escritor.writerow([marca, f"{lectura[0]:.1f}", f"{lectura[1]:.1f}"])
                archivo.flush()
                print(f"{marca}  {lectura[0]:.1f} C  {lectura[1]:.1f} %")
    except KeyboardInterrupt:
        print("\nRegistro detenido.")
    except serial.SerialException as error:
        sys.exit(f"Error de puerto serie: {error}")
    finally:
        archivo.close()


if __name__ == "__main__":
    main()
