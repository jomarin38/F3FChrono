//Plug anemometer between D7 and Ground

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define WIFI_SSID "F3FCtrl"
#define WIFI_PASS "F3FPassword"
#define UDP_PORT 4210

int nDetections =0;
unsigned long lastDetectionTime;
unsigned long currentTime;
float period= 0;
float freq =0;
bool flag = false;
int bufferSize = 3;
float windSpeed = 0.0;

#define batProtectionVoltage 9.6

#define R3 3640.0
#define R4 1000.0

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
  pinMode(D7, INPUT_PULLUP);
  // pinMode(LED_BUILTIN, OUTPUT); 
  attachInterrupt(digitalPinToInterrupt(D7), anemo, RISING);

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

  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 3.2V):
  float voltage = sensorValue * (3.2 / 1023.0);

  float batVoltage = (R3+R4)/R4 * voltage;

  // put your main code here, to run repeatedly:
  if (flag)
  {
    freq = 1000.0/period/3.0;
    flag = false;
    lastDetectionTime = millis();
    windSpeed = 2.4 * freq * 0.277778;
    sendUDP(windSpeed, batVoltage);
  }
  else {
    sendUDP(0.0, batVoltage);
  }
  delay(1000);
}

ICACHE_RAM_ATTR void anemo(void)
{
 nDetections++;
 if (nDetections>= bufferSize)
 {
 currentTime = millis();
 period = float(currentTime-lastDetectionTime)/float(nDetections);
 lastDetectionTime = currentTime;
 flag = true;
 nDetections=0;
 }
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
