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

#define ANALOG_TIMEOUT 30000
unsigned long analogTimeOut;
int analogValue;
float voltage;

void Analog_Start(void){
  analogTimeOut = 0;
}

void Analog_Read(void){
  if ((millis()-analogTimeOut)>ANALOG_TIMEOUT){
    analogValue = analogRead(A0);
    voltage = analogValue*15/1024;
    Serial.print("analog value : ");
    Serial.print(analogValue);
    Serial.print(", ");
    Serial.print(voltage);
    Serial.println("V");
    TcpClient_SendAnalog(voltage);

    analogTimeOut = millis();
  }
}
