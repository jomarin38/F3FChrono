 /** 
 # This file is part of the F3FDCDisplay distribution (https://github.com/ADU).
 # Copyright (c) 2024 Sylvain DAVIET, Joel MARIN.
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

#ifndef STASSID
  #define STASSID "SDHomeServ"
  #define STAPSK "19762018"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;
#ifndef F3FSERVER_HOST
  #define F3FSERVER_HOST "192.168.0.11"
  #define F3FSERVER_PORT 10000

#endif

#define REQUESTIMEOUT 1000

enum TcpClientStatusEnum{
    Init = 0,
    Listen,
    Accepted,
    Connected,
    InProgress,
    Close,
    WaitBeforeRestart
};

enum BtnEnum{
  Valid=0,
  Cancel,
  Refly,
  Null,
  P100,
  P1000
};

const char* host = F3FSERVER_HOST;
const uint16_t port = F3FSERVER_PORT;
TcpClientStatusEnum TcpClientStatus = Init;
unsigned long timeout = millis();
WiFiClient client;
char responseString[1024]="";

void TCPClient_StartWifi(void)
{
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  TcpClientStatus = Init;
}

void TCPClient_Run(void)
{
  if (TcpClientStatus==Init){
    Serial.print("connecting to ");
    Serial.print(host);
    Serial.print(':');
    Serial.println(port);
  
    // Use WiFiClient class to create TCP connections

    if (!client.connect(host, port)) {
      Serial.println("connection failed");
      timeout = millis();
      TcpClientStatus = WaitBeforeRestart;
    }else{
      TcpClientStatus = Connected;
    }
  }

  if (TcpClientStatus==Connected){
    // This will send a string to the server
    Serial.println("Status Connected = sending \"F3FDCDisplay\" to server");
    if (client.connected()) { 
      client.println("F3FDCDisplay");
      
      // wait for data to be available
      timeout = millis();
      while (client.available() == 0) {
        if (millis() - timeout > REQUESTIMEOUT) {
          Serial.println(">>> Client Timeout !");
          TcpClientStatus = Close;
          return;
        }
      }
        
      
      TcpClientGetResponse();
      Serial.println(responseString);
      if (strcmp(responseString, "F3FDCDisplayServerStarted")==0){
        TcpClientStatus = InProgress;
        Serial.println("Status InProgress Waiting data from server");
      }
    }else{
      TcpClientStatus = Close;
    }
  }
  
  if (TcpClientStatus==InProgress){
    if (client.connected()) { 
      TcpClientGetResponse();
      TcpClientPrintResponseString();
    }else{
      TcpClientStatus = Close;
    }
  }
 
  if (TcpClientStatus==Close){
    // Close the connection
    Serial.println();
    Serial.println("closing connection");
    client.stop(); 
    timeout = millis();
    TcpClientStatus = WaitBeforeRestart;
  }
  
  if (TcpClientStatus==WaitBeforeRestart){
    if (millis() - timeout > 30000) { //Wait a moment
      TcpClientStatus = Init;
    }
  }

}
void TcpClientGetResponse(void)
{
  int i;
  int nbData;
  
  memset (responseString,0,sizeof(responseString)/sizeof(char));
  nbData = client.available();
  for (i=0; i<nbData; i++){
    responseString[i] = client.read();
  }
}

void TcpClientPrintResponseString(void)
{
  if (strlen(responseString)>0){
    Serial.println("Server Data received : ");
    Serial.println(responseString);
  }
}

void TcpClient_SendBP(int btn)
{
  if (client.connected()) { 
    if (btn == Valid){
      Serial.println("BP Valid detection");
      client.println("Valid");
    }
    if (btn == Cancel){
      Serial.println("BP Cancel detection");
      client.println("Cancel");
    }
    if (btn == Refly){
      Serial.println("BP Refly detection");
      client.println("Refly");
    }
    if (btn == Null){
      Serial.println("BP NullFlight detection");
      client.println("NullFlight");
    }
    if (btn == P100){
      Serial.println("BP P100 detection");
      client.println("P100");
    }
    if (btn == P1000){
      Serial.println("BP P1000 detection");
      client.println("P1000");
    } 
  }
}

void TcpClient_SendAnalog(float value)
{
  if (client.connected()){
    char chaine[50]="";
    sprintf(chaine, "analog : %0.1f", value);
    client.println(chaine);
}
}
