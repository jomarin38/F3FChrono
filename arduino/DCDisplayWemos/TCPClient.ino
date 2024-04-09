 /** 
 # This file is part of the F3F distribution (https://github.com/jomarin38/F3FChrono).
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


/*#ifndef STASSID
  #define STASSID "YOURSSID"
  #define STAPSK "YOURPWD"
#endif
*/
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
  DebugStr(DEBUG_START, DEBUG_LN, "TCP Module Start");

  // We start by connecting to a WiFi network
  DebugStr(DEBUG_START, DEBUG_LN, "");
  DebugStr(DEBUG_START, DEBUG_LN, "");
  DebugStr(DEBUG_START, DEBUG_NOLN, "Connecting to ");
  DebugStr(DEBUG_NOSTART, DEBUG_LN, ssid);
  displaySendLine("2", "Awaiting wifi");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ".");;
  }

  DebugStr(DEBUG_START, DEBUG_LN, "");
  DebugStr(DEBUG_START, DEBUG_LN, "WiFi connected");
  DebugStr(DEBUG_START, DEBUG_NOLN, "IP address: ");
  TcpClient_GetlocalIpToString();
  DebugStr(DEBUG_NOSTART, DEBUG_LN, tmpStr);
  display_sendWifiConnected (tmpStr);
  TcpClientStatus = Init;
}

void TCPClient_Run(void)
{
  int dataReceived=0;
  if (TcpClientStatus==Init){
    DebugStr(DEBUG_START, DEBUG_NOLN, "connecting to ");
    DebugStr(DEBUG_NOSTART, DEBUG_NOLN, host);
    DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ":");
    sprintf(tmpStr, "%i", port);
    DebugStr(DEBUG_NOSTART, DEBUG_LN, tmpStr);

  
    // Use WiFiClient class to create TCP connections

    if (!client.connect(host, port)) {
      DebugStr(DEBUG_START, DEBUG_LN, "connection failed");
      timeout = millis();
      TcpClientStatus = WaitBeforeRestart;
    }else{
      TcpClientStatus = Connected;
    }
  }

  if (TcpClientStatus==Connected){
    // This will send a string to the server
    DebugStr(DEBUG_START, DEBUG_LN, "Status Connected - sending \"F3F\" to server");
    if (client.connected()) { 
      client.println("F3FDCDisplay");
      
      // wait for data to be available
      timeout = millis();
      while (client.available() == 0) {
        if (millis() - timeout > REQUESTIMEOUT) {
          DebugStr(DEBUG_START, DEBUG_LN, ">>> Client Timeout !");
          TcpClientStatus = Close;
          return;
        }
      }
        
      
      if (TcpClientGetResponse()>0){
        //DebugStr(DEBUG_START, DEBUG_LN, responseString);
        if (strcmp(responseString, "F3FDCDisplayServerStarted")==0){
          TcpClientStatus = InProgress;
          DebugStr(DEBUG_START, DEBUG_LN, "Status InProgress - Waiting data from server");
        }
      }
    }else{
      TcpClientStatus = Close;
    }
  }
  
  if (TcpClientStatus==InProgress){
    if (client.connected()) { 
      if (TcpClientGetResponse()>0){
        TcpClientPrintResponseString();
        displaySendDataFromServer(responseString);
      }
    }else{
      TcpClientStatus = Close;
    }
  }
 
  if (TcpClientStatus==Close){
    // Close the connection
    DebugStr(DEBUG_NOSTART, DEBUG_LN, "");
    DebugStr(DEBUG_START, DEBUG_LN, "connection has been closed");
    client.stop(); 
    timeout = millis();
    TcpClientStatus = WaitBeforeRestart;

    displaySendClear();
    displaySendDCJudgeDisplay();
    TcpClient_GetlocalIpToString();    
    display_sendWifiConnected (tmpStr);
  }
  
  if (TcpClientStatus==WaitBeforeRestart){
    if (millis() - timeout > 30000) { //Wait a moment
      TcpClientStatus = Init;
    }
  }

}

int TcpClientGetResponse(void)
{
  int i;
  int nbData;
  
  memset (responseString,0,sizeof(responseString)/sizeof(char));
  nbData = client.available();
  for (i=0; i<nbData; i++){
    responseString[i] = client.read();
  }
  return nbData;
}

void TcpClientPrintResponseString(void)
{
  if (strlen(responseString)>0){
    DebugStr(DEBUG_START, DEBUG_NOLN, "Server Data received : ");
    DebugStr(DEBUG_NOSTART, DEBUG_LN, responseString);
  }
}

void TcpClient_SendBP(int btn)
{
  if (client.connected()) { 
    if (btn == Valid){
      DebugStr(DEBUG_START, DEBUG_LN, "BP Valid detection");
      client.println("Valid");
    }
    if (btn == Cancel){
      DebugStr(DEBUG_START, DEBUG_LN, "BP Cancel detection");
      client.println("Cancel");
    }
    if (btn == Refly){
      DebugStr(DEBUG_START, DEBUG_LN, "BP Refly detection");
      client.println("Refly");
    }
    if (btn == Null){
      DebugStr(DEBUG_START, DEBUG_LN, "BP NullFlight detection");
      client.println("NullFlight");
    }
    if (btn == P100){
      DebugStr(DEBUG_START, DEBUG_LN, "BP P100 detection");
      client.println("P100");
    }
    if (btn == P1000){
      DebugStr(DEBUG_START, DEBUG_LN, "BP P1000 detection");
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

void TcpClient_GetlocalIpToString(void)
{
  IPAddress ipAddress = WiFi.localIP();
  sprintf(tmpStr, "%i.%i.%i.%i", ipAddress[0], ipAddress[1], ipAddress[2], ipAddress[3]);
}
