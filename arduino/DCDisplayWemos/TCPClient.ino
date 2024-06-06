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



#define NB_SSID       3
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

char ssid[NB_SSID][20] = {"F3FCtrl", STASSID1, STASSID2};
char password[NB_SSID][20] = {"F3FPassword", STAPSK1, STAPSK2};
char f3fserver_host[NB_SSID][20] = {"192.168.1.251", "192.168.0.250", "192.168.100.13"};
int   f3fserver_port[NB_SSID] = {10000, 10000, 10000};

char wifiindex = 0;
bool connected = false;
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
  WiFi.mode(WIFI_STA);
  wifiindex=0;
  while(!connected)
  {
    DebugStr(DEBUG_START, DEBUG_NOLN, "Connecting to ");
    DebugStr(DEBUG_NOSTART, DEBUG_LN, ssid[wifiindex]);
    displaySendAwaitingWifi(ssid[wifiindex]);
    timeout = 0;
    WiFi.begin(ssid[wifiindex], password[wifiindex]);
    while (WiFi.status() != WL_CONNECTED & timeout<10000) {
      delay(500);
      timeout+=500;
      DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ".");
    }
    if (WiFi.status() == WL_CONNECTED){
      connected = true;
    }else{
      wifiindex = (wifiindex+1)%NB_SSID;
    }
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
    DebugStr(DEBUG_NOSTART, DEBUG_NOLN, f3fserver_host[wifiindex]);
    DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ":");
    sprintf(tmpStr, "%i", f3fserver_port[wifiindex]);
    DebugStr(DEBUG_NOSTART, DEBUG_LN, tmpStr);

  
    // Use WiFiClient class to create TCP connections

    if (!client.connect(f3fserver_host[wifiindex], f3fserver_port[wifiindex])) {
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
    if (millis() - timeout > 5000) { //Wait a moment
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
