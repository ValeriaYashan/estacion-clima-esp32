#!/usr/bin/env python3
"""Genera datos/ejemplo.csv con 24 h de lecturas sinteticas para probar graficar.py.

Los valores son simulados (ciclo diario de temperatura, humedad inversa y algo de
ruido). No son mediciones reales.
"""

import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "datos" / "ejemplo.csv"


def main():
    random.seed(7)
    inicio = datetime(2026, 10, 10, 0, 0, 0)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["fecha_hora", "temperatura_c", "humedad_pct"])
        for paso in range(24 * 6 + 1):
            momento = inicio + timedelta(minutes=10 * paso)
            hora = momento.hour + momento.minute / 60
            ciclo = math.sin((hora - 9) / 24 * 2 * math.pi)
            temperatura = 19.5 + 5.5 * ciclo + random.uniform(-0.2, 0.2)
            humedad = 62.0 - 15.0 * ciclo + random.uniform(-0.8, 0.8)
            escritor.writerow([momento.isoformat(timespec="seconds"), f"{temperatura:.1f}", f"{humedad:.1f}"])
    print(f"Generado {SALIDA}")


if __name__ == "__main__":
    main()
