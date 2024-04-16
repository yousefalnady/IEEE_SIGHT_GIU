#define BLYNK_TEMPLATE_ID "TMPL2yx4rEhPh"
#define BLYNK_TEMPLATE_NAME "Quickstart Template"
#include <WiFi.h>
#include <BlynkSimpleEsp32.h>

#define BLYNK_AUTH_TOKEN "ln8bBlrmzsogFRnsAy0rjsbMbAd-UJIb"
#define BUZZER_PIN 12 // Example buzzer pin

char ssid[] = "Tasneem’s iPhone";
char pass[] = "tasneem4";

void setup() {
  pinMode(BUZZER_PIN, OUTPUT); // Set buzzer pin as output
  Serial.begin(115200);
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass); // Connect to Wi-Fi and Blynk server
}

void loop() {
  Blynk.run(); // Continuously check for incoming commands from the Blynk app
}

BLYNK_WRITE(V0) { // Blynk virtual pin callback function
  int buzzerState = param.asInt(); // Get the value of the virtual pin
  digitalWrite(BUZZER_PIN, buzzerState); // Turn the buzzer on or off
}
