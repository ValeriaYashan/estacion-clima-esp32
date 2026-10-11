#pragma once

// Pin de datos del DHT22 (GPIO del ESP32).
#define PIN_DHT 4

// Tiempo entre lecturas, en milisegundos. El DHT22 admite como minimo 2000.
#define INTERVALO_MS 10000UL

// Wi-Fi opcional: con 1 el ESP32 expone los datos en http://<ip>/datos.json.
// Las credenciales van en src/secrets.h (copiar secrets.example.h). Ese
// archivo esta en .gitignore para no subir contrasenas al repositorio.
#define USAR_WIFI 0

#if USAR_WIFI
#if __has_include("secrets.h")
#include "secrets.h"
#else
#error "Falta src/secrets.h: copia secrets.example.h y completa tus datos."
#endif
#endif
