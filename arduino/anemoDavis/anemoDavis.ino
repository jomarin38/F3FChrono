//Plug anemometer between D7 and Ground

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define WIFI_SSID "F3FCtrl"
#define WIFI_PASS "F3FPassword"
#define UDP_PORT 4210

#define BUFFER_SIZE 5 


volatile unsigned long nDetections = 0;
volatile unsigned long contactBounceTime=0; // Timer to avoid contact bounce in isr 

unsigned long nDetections_copy= 0;
unsigned long dt = 0;
float windSpeed = 0.0;
int windDirection = 0;

const long interval = 1000;
unsigned long previousMillis = 0;  
#define VANE_OFFSET 0; // define the anemometer offset from magnetic north 

//UDP
WiFiUDP udp;
char remoteIP[] = "255.255.255.255";
int remotePort = 4445;
char  message[45] = "";       // a string to send
char  speed_str[8];
char  voltage[8];

void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  // installation interruption D6 pour anemo
  pinMode(D6, INPUT_PULLUP);
  // pinMode(LED_BUILTIN, OUTPUT); 
  attachInterrupt(digitalPinToInterrupt(D6), anemo, RISING);

  // Begin WiFi
  
  WiFi.begin(WIFI_SSID, WIFI_PASS);
   
  // Connecting to WiFi...
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  // Loop continuously while WiFi is not connected
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(100);
    Serial.print(".");
  }
   
  // Connected to WiFi
  Serial.println();
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());

  
}

void loop() {

  windDirection = getWindDirection();

  unsigned long currentMillis = millis();
  dt = currentMillis - previousMillis;

  if (dt > interval) {
    noInterrupts();
    nDetections_copy = nDetections;
    nDetections = 0;
    interrupts();
  
    previousMillis = millis();
  
    if (nDetections_copy>0) {
      windSpeed = 2250.0 * float(nDetections_copy)/float(dt) * 0.44 / 1.8;
    }
    else {
      windSpeed = 0.0;
    }
    sendUDP(windSpeed, 12.0);
    delay(800);
    sendUDPDir(windDirection, 12.0);
    delay(200);
  }
}

ICACHE_RAM_ATTR void anemo(void)
{
    nDetections++;
    contactBounceTime = millis();
}

void sendUDP(float wind_speed, float batVoltage) {
  dtostrf(wind_speed,5,2,speed_str);
  dtostrf(batVoltage,5,2,voltage);
  
  sprintf(message,"wind_speed %s m/s %s\r\n",speed_str,voltage);
  //sprintf(message,"wind_speed %d  %s\r\n",int(wind_speed),voltage);
  
  udp.beginPacket(remoteIP, remotePort);
  udp.write(message);
  udp.endPacket();

  Serial.println(message);
}

void sendUDPDir(int wind_dir, float batVoltage) {
  dtostrf(batVoltage,5,2,voltage);
  
  sprintf(message,"wind_dir %d %s\r\n",wind_dir,voltage);
  
  udp.beginPacket(remoteIP, remotePort);
  udp.write(message);
  udp.endPacket();

  Serial.println(message);
}


// Get Wind Direction 
int getWindDirection() { 
  int windDirection;
  int R2 = 10000;

  int vaneValue = analogRead(A0); 
  float vout = 5.0 * float(vaneValue) / 1023.0;
  if (vout<1.53) {
    windDirection = 183.6 - 120.0 * vout; 
  }
  else {
    windDirection = 149.6739 - 97.8261 * vout; 
  }
  
  if(windDirection > 180) windDirection = windDirection - 360; 
  if(windDirection < -180) windDirection = windDirection + 360;  

  return windDirection;

} 
