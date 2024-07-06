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
#define VERSION "0.1"
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
bool d2state=true;

void setup() {
  delay(500);
  serial_setup();
  displayStart();
}

void loop() {
  serial_run();
  delay(50);
}
void d2_init(){
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
}
