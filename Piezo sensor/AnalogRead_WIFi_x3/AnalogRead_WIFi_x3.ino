#include <ESP8266WiFi.h>
 
// replace with your network credentials
const char* ssid     = "Taj Mahal 2";
const char* password = "GoldenMine124";
 
// replace with your server's IP address and port
IPAddress serverIP(192, 168, 231, 146);
const int serverPort = 8000;
 
WiFiServer server(serverPort);
WiFiClient client;

const int num_samples = 200;
int samples[num_samples];
int data;

String arrayToString(int* array, int len) {
  String str = "";
  for (int i = 0; i < len; i++) {
    str += String(array[i]);
    if (i != len - 1) {
      str += ",";
    }
  }
  return str;
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  server.begin();
  Serial.print("Server started on port ");
  Serial.println(serverPort);
}
 
void loop() {
  client = server.available();
  for (int i = 0; i < num_samples; i++) {
    data = analogRead(A0);
    delay(10);
    samples[i] = data;
    // Serial.println(samples[i]);
  }
  // float mil1 = millis();
  while (!client) {
    // String data = "Hello from ESP8266!";
    client = server.available();
    // Serial.println("Data send");
    // Serial.println(millis() - mil1);
  }
  client.println(arrayToString(samples, num_samples));
  delay(10);
  // delay(1000);
}