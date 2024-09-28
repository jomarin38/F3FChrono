//Plug anemometer between D7 and Ground

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define WIFI_SSID "F3FCtrl"
#define WIFI_PASS "F3FPassword"
#define UDP_PORT 4210

#define BUFFER_SIZE 5 

#define batProtectionVoltage 9.6

#define R3 3640.0
#define R4 1000.0

volatile unsigned long nDetections = 0;

unsigned long nDetections_copy= 0;
unsigned long dt = 0;
float period;
float freq =0;
float windSpeed = 0.0;

const long interval = 5000;
unsigned long previousMillis = 0;  



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

  unsigned long currentMillis = millis();
  dt = currentMillis - previousMillis;

  if (dt >= interval) {

    noInterrupts();
    nDetections_copy = nDetections;
    nDetections = 0;
    interrupts();

    previousMillis = millis();

    // read the input on analog pin 0:
    int sensorValue = analogRead(A0);
    // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 3.2V):
    float voltage = sensorValue * (3.2 / 1023.0);
  
    float batVoltage = (R3+R4)/R4 * voltage;
  
    // put your main code here, to run repeatedly:
    if (nDetections_copy>0) {
      windSpeed = nDetections_copy * 0.9 * 0.447 * 2.4 * dt / 1000.0;
      //period = float(dt)/float(nDetections_copy);
      //freq = 1000.0/period/3.0;
      //windSpeed = 2.4 * freq * 0.277778;
    }
    else {
      windSpeed = 0.0;
    }
    sendUDP(windSpeed, 11.3);
    delay(1000);
    sendWindDir(0,11.3);
    
  }
}

ICACHE_RAM_ATTR void anemo(void)
{
 nDetections++;
}

void sendUDP(float wind_speed, float batVoltage) {
  dtostrf(wind_speed,5,2,speed_str);
  dtostrf(batVoltage,5,2,voltage);
  
  sprintf(message,"wind_speed %s m/s %s\r\n",speed_str,voltage);
  //sprintf(message,"wind_speed %d  %s\r\n",int(wind_speed),voltage);
  
  udp.beginPacket(remoteIP, remotePort);
  udp.write(message);
  udp.endPacket();

  //Serial.println(message);
}

void sendWindDir(int angle, float batVoltage) {
  dtostrf(batVoltage,5,2,voltage);
  
  sprintf(message,"wind_dir %d %s\r\n",angle,voltage);
  //sprintf(message,"wind_speed %d  %s\r\n",int(wind_speed),voltage);
  
  udp.beginPacket(remoteIP, remotePort);
  udp.write(message);
  udp.endPacket();

  //Serial.println(message);
}
