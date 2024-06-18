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

#define ANALOG_TIMEOUT 300000
unsigned long analogTimeOut=0;
int analogValue;
float voltage;
bool firstvoltage;

void Analog_Start(void){
  DebugStr(DEBUG_START, DEBUG_LN, "Analog Module Start");
  analogTimeOut = 0;
  analogValue = 0;
  voltage= 0;
  firstvoltage=true;
}

void Analog_Read(void){
  if ((millis()-analogTimeOut)>ANALOG_TIMEOUT or firstvoltage){
    analogValue = analogRead(A0);
    voltage = analogValue/1024*1.28;
    sprintf(tmpStr, "analog value:%i, %.1fV", analogValue, voltage);
    Serial.println(tmpStr);
    DebugStr(DEBUG_START, DEBUG_LN, tmpStr);
    //TcpClient_SendAnalog(voltage);
    firstvoltage = false;
    analogTimeOut = millis();
  }
}

void Analog_getVoltage(float *data)
{
  *data = float (analogValue);
}
