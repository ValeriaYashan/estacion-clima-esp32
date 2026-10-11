#!/usr/bin/env python3
"""Grafica temperatura y humedad a partir del CSV generado por registrar.py.

Uso:
    python software/graficar.py --entrada datos/lecturas.csv --horas 24 --salida grafico.png
    python software/graficar.py --entrada datos/ejemplo.csv --mostrar
"""

import argparse
import csv
import sys
from datetime import datetime, timedelta

import matplotlib

COLOR_TEMPERATURA = "#D85A30"
COLOR_HUMEDAD = "#378ADD"


def leer_csv(ruta):
    """Devuelve tres listas: fechas, temperaturas y humedades."""
    fechas, temperaturas, humedades = [], [], []
    with open(ruta, newline="", encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):
            try:
                fechas.append(datetime.fromisoformat(fila["fecha_hora"]))
                temperaturas.append(float(fila["temperatura_c"]))
                humedades.append(float(fila["humedad_pct"]))
            except (KeyError, ValueError):
                continue
    return fechas, temperaturas, humedades


def filtrar_ultimas_horas(fechas, temperaturas, humedades, horas):
    """Se queda con las ultimas `horas` respecto de la lectura mas reciente."""
    if not fechas or horas is None:
        return fechas, temperaturas, humedades
    limite = max(fechas) - timedelta(hours=horas)
    indices = [i for i, f in enumerate(fechas) if f >= limite]
    return (
        [fechas[i] for i in indices],
        [temperaturas[i] for i in indices],
        [humedades[i] for i in indices],
    )


def graficar(fechas, temperaturas, humedades, horas, salida, mostrar):
    if not mostrar:
        matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    fig, eje_t = plt.subplots(figsize=(10, 4.5), dpi=150)
    eje_h = eje_t.twinx()

    eje_t.plot(fechas, temperaturas, color=COLOR_TEMPERATURA, linewidth=1.8, label="Temperatura")
    eje_h.plot(fechas, humedades, color=COLOR_HUMEDAD, linewidth=1.8, label="Humedad")

    eje_t.set_ylabel("Temperatura (°C)", color=COLOR_TEMPERATURA)
    eje_h.set_ylabel("Humedad relativa (%)", color=COLOR_HUMEDAD)
    eje_t.tick_params(axis="y", colors=COLOR_TEMPERATURA)
    eje_h.tick_params(axis="y", colors=COLOR_HUMEDAD)
    eje_t.set_title(
        f"Estación de medición, últimas {horas} h" if horas else "Estación de medición",
        pad=28,
    )
    eje_t.grid(True, alpha=0.25)
    eje_t.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))
    fig.autofmt_xdate()

    lineas = eje_t.get_lines() + eje_h.get_lines()
    eje_t.legend(
        lineas,
        [l.get_label() for l in lineas],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.0),
        ncol=2,
        frameon=False,
    )

    fig.tight_layout()
    if salida:
        fig.savefig(salida)
        print(f"Grafico guardado en {salida}")
    if mostrar:
        plt.show()
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", default="datos/lecturas.csv")
    parser.add_argument("--horas", type=float, default=24, help="Ventana a graficar; 0 grafica todo")
    parser.add_argument("--salida", default="grafico.png")
    parser.add_argument("--mostrar", action="store_true", help="Abrir la ventana del grafico")
    args = parser.parse_args()

    horas = args.horas if args.horas > 0 else None
    try:
        fechas, temperaturas, humedades = leer_csv(args.entrada)
    except FileNotFoundError:
        sys.exit(f"No existe {args.entrada}. Generalo con registrar.py o usa datos/ejemplo.csv.")

    fechas, temperaturas, humedades = filtrar_ultimas_horas(fechas, temperaturas, humedades, horas)
    if not fechas:
        sys.exit("No hay lecturas validas para graficar.")

    graficar(fechas, temperaturas, humedades, int(args.horas) if horas else None, args.salida, args.mostrar)


if __name__ == "__main__":
    main()
