#include <Arduino.h>
#include <DHT.h>

#include "config.h"

#if USAR_WIFI
#include <WebServer.h>
#include <WiFi.h>
#endif

static DHT dht(PIN_DHT, DHT22);

static float ultimaTemperatura = NAN;
static float ultimaHumedad = NAN;
static unsigned long ultimaLectura = 0;

#if USAR_WIFI
static WebServer servidor(80);

static void responderDatos() {
  char cuerpo[96];
  if (isnan(ultimaTemperatura) || isnan(ultimaHumedad)) {
    servidor.send(503, "application/json", "{\"error\":\"sin lecturas\"}");
    return;
  }
  snprintf(cuerpo, sizeof(cuerpo),
           "{\"temperatura_c\":%.1f,\"humedad_pct\":%.1f,\"tiempo_ms\":%lu}",
           ultimaTemperatura, ultimaHumedad, ultimaLectura);
  servidor.send(200, "application/json", cuerpo);
}

static void conectarWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("# Conectando a Wi-Fi");
  unsigned long inicio = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - inicio < 20000UL) {
    delay(500);
    Serial.print('.');
  }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("# IP: ");
    Serial.println(WiFi.localIP());
    servidor.on("/datos.json", responderDatos);
    servidor.begin();
  } else {
    Serial.println("# No se pudo conectar. Sigue funcionando por serial.");
  }
}
#endif

void setup() {
  Serial.begin(115200);
  delay(500);
  dht.begin();
#if USAR_WIFI
  conectarWifi();
#endif
  // Cabecera del CSV. Las lineas que empiezan con # son mensajes de estado.
  Serial.println("tiempo_ms,temperatura_c,humedad_pct");
}

void loop() {
#if USAR_WIFI
  servidor.handleClient();
#endif

  unsigned long ahora = millis();
  if (ahora - ultimaLectura < INTERVALO_MS && ultimaLectura != 0) {
    return;
  }

  float humedad = dht.readHumidity();
  float temperatura = dht.readTemperature();

  if (isnan(humedad) || isnan(temperatura)) {
    Serial.println("# error de lectura del DHT22");
    ultimaLectura = ahora;
    return;
  }

  ultimaTemperatura = temperatura;
  ultimaHumedad = humedad;
  ultimaLectura = ahora;

  Serial.printf("%lu,%.1f,%.1f\n", ahora, temperatura, humedad);
}
