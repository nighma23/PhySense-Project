#include <HCSR04.h>
#include <WiFi.h>


const char* ssid     = "Taj Mahal 2";
const char* password = "GoldenMine124";
 
IPAddress serverIP(192, 168, 231, 83);
const int serverPort = 8000;
 
WiFiServer server(serverPort);
WiFiClient client;

const int midle_point_Cm = 10;
const int midle_range_Cm = 3;
const int max_distance_Cm = 20;

const int triggerPin_1 = 33;
const int echoPin_1 = 15;
UltraSonicDistanceSensor distanceSensor_1(triggerPin_1, echoPin_1);

const int triggerPin_2 = 14;
const int echoPin_2 = 32;
UltraSonicDistanceSensor distanceSensor_2(triggerPin_2, echoPin_2);

const int triggerPin_3 = 27;
const int echoPin_3 = 12;
int distance_3 = 0;
UltraSonicDistanceSensor distanceSensor_3(triggerPin_3, echoPin_3);

int get_pos();
bool should_zoom_in();
bool should_zoom_out();
bool should_move_right();
bool should_move_left();
bool should_move_up();
bool should_move_down();

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
    String output = "";
    if (should_zoom_in())
      output = "ZoomIn";
    else if (should_zoom_out())
      output = "ZoomOut";
    else if (should_move_right())
      output = "MoveRight";
    else if (should_move_left())
      output = "MoveLeft";
    else if (should_move_up())
      output = "MoveUp";
    else if (should_move_down())
      output = "MoveDown";
    else if (should_reset())
      output = "Reset";
    Serial.println(output);
    client.println(output);
  }
  delay(10);
}

bool should_zoom_in() {
  if ((get_pos(distanceSensor_1) == -1) &&
      (get_pos(distanceSensor_2) == -1) &&
      (get_pos(distanceSensor_3) == -1))
    return true;
  return false;
}

bool should_zoom_out() {
  if ((get_pos(distanceSensor_1) == 1) &&
      (get_pos(distanceSensor_2) == 1) &&
      (get_pos(distanceSensor_3) == 1))
    return true;
  return false;
}

bool should_move_right() {
  if ((get_pos(distanceSensor_1) != 0) &&
      (get_pos(distanceSensor_2) == 0) &&
      (get_pos(distanceSensor_3) == 0))
    return true;
  return false;
}

bool should_move_left() {
  if ((get_pos(distanceSensor_1) == 0) &&
      (get_pos(distanceSensor_2) != 0) &&
      (get_pos(distanceSensor_3) == 0))
    return true;
  return false;
}

bool should_move_up() {
  if ((get_pos(distanceSensor_1) == 0) &&
      (get_pos(distanceSensor_2) == 0) &&
      (get_pos(distanceSensor_3) != 0))
    return true;
  return false;
}

bool should_move_down() {
  if ((get_pos(distanceSensor_1) != 0) &&
      (get_pos(distanceSensor_2) != 0) &&
      (get_pos(distanceSensor_3) == 0))
    return true;
  return false;
}

bool should_reset() {
  if ((get_pos(distanceSensor_1) == 2) &&
      (get_pos(distanceSensor_2) == 2) &&
      (get_pos(distanceSensor_3) == 2))
    return true;
  return false;
}

int get_pos(UltraSonicDistanceSensor distanceSensor) {
  int d = distanceSensor.measureDistanceCm();
  bool is_no_input = d > max_distance_Cm;
  bool is_middle = abs(d - midle_point_Cm) < midle_range_Cm;
  bool is_up = d > midle_point_Cm + midle_range_Cm;
  bool is_bottom = d < midle_point_Cm - midle_range_Cm;

  if (is_no_input) return 0;
  if (is_middle) return 2;
  if (is_up) return 1;
  if (is_bottom) return -1;
  return 0; // to be sure
}
