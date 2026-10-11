# Cableado

El DHT22 se conecta al ESP32 con tres cables. Todo funciona a 3,3 V.

| DHT22 | ESP32 DevKit |
|-------|--------------|
| VCC (+) | 3V3 |
| DATA (OUT) | GPIO 4 |
| GND (-) | GND |

Si usás el sensor suelto, de cuatro patas, hace falta una resistencia pull-up de 10 kΩ entre DATA y VCC. Las placas de tres pines ya la traen incorporada. El pin de datos se cambia en `firmware/src/config.h` (`PIN_DHT`).

## Cosas a tener en cuenta

El DHT22 tiene una precisión nominal de ±0,5 °C en temperatura y entre ±2 % y ±5 % en humedad relativa, según la hoja de datos. Dentro de una caja cerrada, el propio ESP32 se calienta, sobre todo con el Wi-Fi activo, y puede sumar algún grado a la lectura. Por eso el diseño ubica el sensor del lado de las ventilas y lejos de la placa. Para una medición confiable, compará contra un termómetro de referencia unas horas y, si hace falta, restá el desvío en el script.

El sensor no debe leerse más de una vez cada 2 segundos. El intervalo por defecto es de 10 segundos (`INTERVALO_MS`).
