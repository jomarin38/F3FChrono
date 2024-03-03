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




void setup() {
  Serial.begin(115200);
  TCPClient_StartWifi();
  BP_Start();
  Analog_Start();
}

void loop() {
  TCPClient_Run();
  BP_CheckChanged();
  Analog_Read();
  delay(50);
}
