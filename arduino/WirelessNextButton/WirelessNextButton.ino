#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#ifndef STASSID
  #define STASSID "F3FCtrl"
  #define STAPSK  "F3FPassword"
#endif


// buffers for receiving and sending data
char  message_wBtn[] = "";       // a string to send

char remoteIP[] = "255.255.255.255";
int remotePort = 4445;

const int buttonPin = 2;
int buttonState = 0;
int count=0;
WiFiUDP Udp;

bool buttonReleased;
bool buttonPressed;

enum Event {
  pressed,
  clicked,
  longPressed
};

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

  buttonReleased = true;
  buttonPressed = false;
  
}

void sendMessage(Event e) {
  strcpy (message_wBtn, "wBtn ");
  if (e==pressed) {
    strcat (message_wBtn, "-1");
  }
  else if (e==clicked) {
    strcat (message_wBtn, "1");
  }
  else if (e==longPressed) {
    strcat (message_wBtn, "0");
  }
  strcat (message_wBtn, "\r\n");
  Udp.beginPacket(remoteIP, remotePort);
  Udp.write(message_wBtn);
  Udp.endPacket();
}

void loop() {

  buttonState = digitalRead(buttonPin);

  if (buttonState == LOW) {
    if (buttonReleased && count==0) {
      sendMessage(pressed);
      buttonReleased=false;
      buttonPressed=true;
      count++;
    }
    else if (count>=100) {
      sendMessage(longPressed);
      count = 0 ;
      buttonPressed=false;
    }
    else if (buttonPressed) {
      count++;
    }
  }else if (buttonState == HIGH) {
    if (buttonPressed && count>0 && count<=100) {
      sendMessage(clicked);
    }
    count = 0;
    buttonReleased = true;
    buttonPressed = false;
  }
  delay(10);
}
