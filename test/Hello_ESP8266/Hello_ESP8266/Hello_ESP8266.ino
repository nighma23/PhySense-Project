#include <ESP8266WiFi.h>
 
const char* ssid     = "Taj Mahal 2";
const char* password = "GoldenMine124";
 
IPAddress serverIP(192, 168, 231, 171);
const int serverPort = 8000;
 
WiFiServer server(serverPort);
WiFiClient client;
 
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
 
  server.begin();
  Serial.print("Server started on port ");
  Serial.print(serverPort);
  Serial.print(" with IP ");
  Serial.println(WiFi.localIP());  
}
 
void loop() {
  client = server.available();
  if (client) {
    String data = "Hello from ESP8266_1!";
    client.println(data);
  }
  delay(1000);
}