# Estación de medición con ESP32

Estación que registra temperatura y humedad con un ESP32 y un sensor DHT22, guarda las lecturas en un CSV, las grafica con Python y se aloja en una caja diseñada e impresa en 3D.

![Mockup de la estación](docs/mockup.svg)

## Qué incluye

El repositorio tiene tres partes que se pueden usar por separado. En `firmware/` está el programa del ESP32 (PlatformIO, framework Arduino), que lee el DHT22 y publica cada lectura por serial como una línea CSV, con un servidor HTTP opcional por Wi-Fi. En `software/` están los scripts de Python que registran esas lecturas con fecha y hora y arman el gráfico. En `caja/` está el modelo paramétrico en OpenSCAD de la caja, con base, tapa, ventilas frente al sensor y abertura USB.

```
firmware/   programa del ESP32 (PlatformIO)
software/   registrar.py, graficar.py, generar_ejemplo.py
caja/       caja.scad (base y tapa)
datos/      ejemplo.csv (datos simulados) y tus lecturas
docs/       cableado, lista de materiales, mockup
tests/      pruebas de los scripts de Python
```

## Inicio rápido

Conectá el DHT22 al ESP32 según [docs/cableado.md](docs/cableado.md): VCC a 3V3, DATA a GPIO 4 y GND a GND. Después cargá el firmware con PlatformIO:

```bash
pio run -d firmware -t upload
pio device monitor -d firmware
```

En el monitor vas a ver líneas como `12000,23.4,55.1` (milisegundos, °C, % de humedad). Con el ESP32 conectado por USB, instalá las dependencias de Python y registrá las lecturas:

```bash
pip install -r software/requirements.txt
python software/registrar.py --puerto COM3          # en Linux: /dev/ttyUSB0
python software/graficar.py --entrada datos/lecturas.csv --horas 24 --salida grafico.png
```

Para probar el gráfico sin hardware hay datos simulados, no mediciones reales:

```bash
python software/graficar.py --entrada datos/ejemplo.csv --salida docs/grafico_ejemplo.png
```

![Gráfico de ejemplo](docs/grafico_ejemplo.png)

## Wi-Fi opcional

En `firmware/src/config.h` poné `USAR_WIFI` en `1`, copiá `firmware/src/secrets.example.h` como `secrets.h` y completá tu red. El ESP32 va a responder en `http://<ip>/datos.json`. El archivo `secrets.h` está en `.gitignore`, así que tus credenciales no se suben al repositorio.

## La caja

Abrí `caja/caja.scad` en OpenSCAD, elegí `parte = "base"` o `"tapa"` y exportá a STL (F6 y luego F7). Las medidas externas son de unos 87 x 63 x 26,4 mm para la base más 3 mm de tapa. Se imprime sin soportes, con base y tapa apoyadas en la cama. Recomendación de partida: PETG o PLA, capa de 0,2 mm, 3 perímetros y 20 % de relleno. Se cierra con cuatro tornillos M3 autorroscantes. Los parámetros de la placa y del sensor están al inicio del archivo por si usás otros modelos.

## Pruebas

```bash
pip install pytest
pytest tests
```

## Licencia

MIT. Ver [LICENSE](LICENSE).
