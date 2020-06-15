#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#ifndef STASSID
#define STASSID "F3FCtrl"
#define STAPSK  "F3FPassword"
#endif


// buffers for receiving and sending data
char  message[] = "simulate GPIO btnnext\r\n";       // a string to send

char remoteIP[] = "255.255.255.255";
int remotePort = 4445;

const int buttonPin = 2;
int buttonState = 0;

WiFiUDP Udp;

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(STASSID, STAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());

  pinMode(0, OUTPUT);
  digitalWrite(0, LOW);

  pinMode(buttonPin, INPUT);
  
}

void loop() {

  buttonState = digitalRead(buttonPin);

  if (buttonState == LOW) {

    Udp.beginPacket(remoteIP, remotePort);
    Udp.write(message);
    Udp.endPacket();
    delay(500);

  }

}

