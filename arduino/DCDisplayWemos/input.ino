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

const int BP_Pin[6] = {D0, D1, D2, D3, D4, D5};
int btnState[6] = {0};
int btnStateLast[6] = {0};

void BP_Start(void)
{
  Serial.println("BP_Start");
  int i=0;
  for (i=0; i<sizeof(btnState)/sizeof(int); i++){
    pinMode(BP_Pin[i], INPUT_PULLUP);
    //digitalWrite(BP_Pin[i], HIGH); don't work to activate pull_up at each pin ;)
  }
  memset (btnState, 0, sizeof(btnState)/sizeof(int));
  memset (btnStateLast, 0, sizeof(btnStateLast)/sizeof(int));
}


void BP_CheckChanged (void)
{
  int i;
  //Serial.println("BP_CheckChanged");
  for (i=0; i<sizeof(btnState)/sizeof(int); i++){
    btnState[i] = digitalRead (BP_Pin[i]);
    /*Serial.print(btnState[i]);  
    Serial.print(" - ");  
    Serial.print(btnStateLast[i]);
    Serial.print(", ");  
    */
    if (btnState[i] != btnStateLast[i]){
      if (btnState[i] == LOW){
        Serial.print("BP Detection : ");
        Serial.println(i);
        TcpClient_SendBP (i);
      }
    }
    btnStateLast[i] = btnState[i];
  }
  //Serial.println("");
}
