 /** 
 # This file is part of the F3FDCDisplay distribution (https://github.com/jomarin38/F3FChrono).
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

//#define _DEBUG_
#define DEBUG_LN true
#define DEBUG_NOLN false
#define DEBUG_START true
#define DEBUG_NOSTART false

#ifdef _DEBUG_
  static void DebugStr(bool debug, bool ln, const char *str)
  {
    if (debug){
      Serial.print("DEBUG - ");
    }
    if (ln){
      Serial.println(str);  
    }else{
      Serial.print(str);  
    }
  }
#else
  static void DebugStr(bool debug, bool ln, const char *str)
  {
    str;
  }

#endif

char tmpStr[100]="";


void setup() {
  delay(500);
  Serial.begin(57600);
  display_Start();
  BP_Start();
  Analog_Start();
  TCPClient_StartWifi();
}

void loop() {
  TCPClient_Run();
  BP_CheckChanged();
  Analog_Read();
  delay(50);
}
