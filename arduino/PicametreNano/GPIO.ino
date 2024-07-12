 /** 
 # This file is part of the Picametre distribution (https://github.com/jomarin38/F3FChrono).
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


#include <MCP23017.h>

MCP23017 mcp[2];
char temps[4];


void gpio_setup(void){
  /*the param can be 0 to 7,the default param is 7.means the dafault device address 0x27.
  Addr(BIN)  Addr(hex)   param
  010 0111    0x27        7
  010 0110    0x26        6
  010 0101    0x25        5
  010 0100    0x24        4
  010 0011    0x23        3
  010 0010    0x22        2
  010 0001    0x21        1
  010 0000    0x20        0
  */
  mcp[0].begin(7);
  mcp[1].begin(6);
  for(int i=0; i<16; i++)
  {
      mcp[0].pinMode(i, OUTPUT);
      mcp[1].pinMode(i, OUTPUT);
  }

  //writeGPIOAB PA 0xFF, PB 0xFF00
  temps[0]=0;
  temps[1]=8;
  temps[3]=4;
  temps[4]=3;
  mcp[0].writeGPIOAB(0x1111);  
  //gpio_writetime(temps);
  //gpio_notime();
}


void gpio_writetime(char *time){
  int data;
  data = (((time[4]-'0')&0x0F)<<12 | ((time[3]-'0')&0x0F)<<8 | ((time[1]-'0')&0x0F)<<4 | (time[0]-'0')&0x0F);
  gpio_notime();  
  delay(10);
  DebugStr(DEBUG_START, DEBUG_NOLN, "Picametre display data : 0x");
  Serial.println(data, HEX);
  mcp[0].writeGPIOAB(data);    
  gpio_time();  
}

void gpio_notime(void){
  DebugStr(DEBUG_START, DEBUG_LN, "Picametre no time");
  mcp[1].writeGPIOAB(0x00);    
}

void gpio_time(void){
  DebugStr(DEBUG_START, DEBUG_LN, "Picametre display time");
  mcp[1].writeGPIOAB(0x0F);  
}
