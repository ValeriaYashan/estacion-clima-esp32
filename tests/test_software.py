import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "software"))

from graficar import filtrar_ultimas_horas, leer_csv  # noqa: E402
from registrar import parsear_linea  # noqa: E402


def test_parsear_linea_valida():
    assert parsear_linea("12000,23.4,55.1\n") == (23.4, 55.1)


def test_parsear_linea_ignora_cabecera_y_mensajes():
    assert parsear_linea("tiempo_ms,temperatura_c,humedad_pct") is None
    assert parsear_linea("# error de lectura del DHT22") is None
    assert parsear_linea("") is None


def test_parsear_linea_ignora_basura_y_fuera_de_rango():
    assert parsear_linea("12000,abc,55") is None
    assert parsear_linea("12000,23.4") is None
    assert parsear_linea("12000,120.0,55.0") is None
    assert parsear_linea("12000,23.0,140.0") is None


def test_filtrar_ultimas_horas():
    fechas = [datetime(2026, 10, 10, h) for h in (0, 6, 12, 18)]
    f, t, h = filtrar_ultimas_horas(fechas, [1, 2, 3, 4], [10, 20, 30, 40], 7)
    assert t == [3, 4] and h == [30, 40] and len(f) == 2


def test_leer_csv_ejemplo():
    ruta = Path(__file__).resolve().parent.parent / "datos" / "ejemplo.csv"
    fechas, temperaturas, humedades = leer_csv(ruta)
    assert len(fechas) == len(temperaturas) == len(humedades) == 145
