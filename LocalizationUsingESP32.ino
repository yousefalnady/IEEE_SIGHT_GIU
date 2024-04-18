
#include <WiFi.h>
#include <HardwareSerial.h>
const char* SSID = "iPhone";
const char* PASSWORD = "Aisha123";

void connectWiFi() {
  WiFi.begin(SSID, PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1, 16, 17); // RX2 pin is GPIO 17 on ESP32, connect your GPS module to RX2 and TX2
  connectWiFi();
}

void loop() {
  Serial.println("Reading GPS data...");
  if (Serial2.available()) {
    String line = Serial2.readStringUntil('\n');
    if (line.startsWith("$GPGGA")) {
      char *cstr = new char[line.length() + 1];
      strcpy(cstr, line.c_str());
      char *token = strtok(cstr, ",");
      int index = 0;
      float latitude_degrees, latitude_minutes, longitude_degrees, longitude_minutes;
      while (token != NULL) {
        if (index == 2) {
          float latitude = atof(token);
          latitude_degrees = int(latitude / 100);
          latitude_minutes = (latitude - latitude_degrees * 100) / 60.0;
        }
        else if (index == 3 && strcmp(token, "S") == 0) {
          latitude_degrees = -latitude_degrees;
        }
        else if (index == 4) {
          float longitude = atof(token);
          longitude_degrees = int(longitude / 100);
          longitude_minutes = (longitude - longitude_degrees * 100) / 60.0;
        }
        else if (index == 5 && strcmp(token, "W") == 0) {
          longitude_degrees = -longitude_degrees;
        }
        else if (index == 6 && strcmp(token, "") != 0 && strcmp(strtok(NULL, ","), "") != 0 && strcmp(strtok(NULL, ","), "") != 0) {
          float latitude = latitude_degrees + latitude_minutes;
          float longitude = longitude_degrees + longitude_minutes;
          Serial.print("Latitude: ");
          Serial.println(latitude, 6); // Print latitude with 6 decimal places
          Serial.print("Longitude: ");
          Serial.println(longitude, 6); // Print longitude with 6 decimal places
        }
        token = strtok(NULL, ",");
        index++;
      }
      delete[] cstr;
    }
  }
}
