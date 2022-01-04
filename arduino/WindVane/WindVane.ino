 /** 
 # This file is part of the F3FChrono distribution (https://github.com/jomarin38/F3FChrono).
 # Copyright (c) 2021 Sylvain DAVIET, Joel MARIN.
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define WIFI_SSID "F3FCtrl"
#define WIFI_PASS "F3FPassword"
#define UDP_PORT 4210

#define encoder0PinA  12
#define encoder0PinB  13
#define buttonPin     0

#define PULSE_PER_HALF_REVOLUTION 200

#define nSamples 50
#define sleepDelay 100
#define sendDelay 1000

#define batProtectionVoltage 9.6

#define R3 3640.0
#define R4 1000.0

//UDP
WiFiUDP udp;
char remoteIP[] = "255.255.255.255";
int remotePort = 4445;
char  message[45] = "";       // a string to send

volatile int encoder0Pos = 0;

int anglesHistory[nSamples];
int sum = 0;
int historyIndex = 0;

int currentAngle = 0;

int counter = 0;

void setup() {
  pinMode(encoder0PinA, INPUT);
  pinMode(encoder0PinB, INPUT);
  pinMode(buttonPin, INPUT_PULLUP);

  // encoder pin on interrupt 0 (pin 2)
  attachInterrupt(digitalPinToInterrupt(encoder0PinA), doEncoderA, CHANGE);

  // encoder pin on interrupt 1 (pin 3)
  attachInterrupt(digitalPinToInterrupt(encoder0PinB), doEncoderB, CHANGE);

  Serial.begin (115200);
  Serial.println("Start of the program ...");

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

  //Initialize history
  for (int i=0;i<nSamples;i++) {
    anglesHistory[i]=0;
  }
  
}

void loop() {

  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 3.2V):
  float voltage = sensorValue * (3.2 / 1023.0);

  float batVoltage = (R3+R4)/R4 * voltage;

  //Uncomment to calibrate using serial monitor
  //Serial.print("Battery voltage : ");Serial.println(batVoltage);

  if (batVoltage<batProtectionVoltage) {
    sendVoltageAlarm();
  }


  boolean btnPressed = !digitalRead(buttonPin);
  if (btnPressed) {
    Serial.println("Button pressed !");
    encoder0Pos = 0;
  }
  currentAngle = getAngleSmooth();
  counter++;
  if (counter*sleepDelay>sendDelay) {
    sendUDP(currentAngle);
    counter=0;
  }
  delay(sleepDelay);
}

int getAngle() {
  if (encoder0Pos>0) {
    return int(((encoder0Pos+PULSE_PER_HALF_REVOLUTION)%(2*PULSE_PER_HALF_REVOLUTION)
           -PULSE_PER_HALF_REVOLUTION)/
          float(PULSE_PER_HALF_REVOLUTION)*180.0);
  }
  else {
    return int(((encoder0Pos-PULSE_PER_HALF_REVOLUTION)%(2*PULSE_PER_HALF_REVOLUTION)
           +PULSE_PER_HALF_REVOLUTION)/
          float(PULSE_PER_HALF_REVOLUTION)*180.0);
  }
  
}

int getAngleSmooth() {
  sum = sum - anglesHistory[historyIndex];
  anglesHistory[historyIndex]=getAngle();
  sum = sum + anglesHistory[historyIndex];

  if (historyIndex >= nSamples-1) {
    historyIndex = 0;
  }
  else {
    historyIndex++;
  }

  return int(float(sum)/float(nSamples));
}

void sendUDP(int angle) {
  sprintf(message,"wind_dir %d\r\n",angle);
  
  udp.beginPacket(remoteIP, remotePort);
  udp.write(message);
  udp.endPacket();
  
  //Serial.println(message);
}

void sendVoltageAlarm() {
  sprintf(message,"wind_dir_low_voltage\r\n");
  
  udp.beginPacket(remoteIP, remotePort);
  udp.write(message);
  udp.endPacket();
  
  //Serial.println(message);
}

ICACHE_RAM_ATTR void doEncoderA() {
  // look for a low-to-high on channel A
  if (digitalRead(encoder0PinA) == HIGH) {

    // check channel B to see which way encoder is turning
    if (digitalRead(encoder0PinB) == LOW) {
      encoder0Pos = encoder0Pos + 1;         // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;         // CCW
    }
  }

  else   // must be a high-to-low edge on channel A
  {
    // check channel B to see which way encoder is turning
    if (digitalRead(encoder0PinB) == HIGH) {
      encoder0Pos = encoder0Pos + 1;          // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;          // CCW
    }
  }
}

ICACHE_RAM_ATTR void doEncoderB() {
  // look for a low-to-high on channel B
  if (digitalRead(encoder0PinB) == HIGH) {

    // check channel A to see which way encoder is turning
    if (digitalRead(encoder0PinA) == HIGH) {
      encoder0Pos = encoder0Pos + 1;         // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;         // CCW
    }
  }

  // Look for a high-to-low on channel B

  else {
    // check channel B to see which way encoder is turning
    if (digitalRead(encoder0PinA) == LOW) {
      encoder0Pos = encoder0Pos + 1;          // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;          // CCW
    }
  }
}
