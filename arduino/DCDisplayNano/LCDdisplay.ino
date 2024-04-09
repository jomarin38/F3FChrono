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

#include <LiquidCrystal.h>


  LiquidCrystal lcd(3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13); 

void displayStart(void)
{
  DebugStr(DEBUG_START, DEBUG_LN, "display Module Start");
  lcd.begin(20, 4);
  displayClear();
  displayPrintLine(0, "DC Display&JUDGE");
  displayPrintLine(1, "    START TEST");
  displayPrintLine(2, "01234567890123456789");
  displayPrintLine(3, "01234567890123456789");
}

void displayClear(void)
{
  lcd.clear();
}

void displayPrintLine(int line, char *str)
{
  char strtmp[21]={0};
  int i;

  lcd.setCursor(0, line);
  strcpy(strtmp, str);
  //Add space char for the end of line
  for (i=strlen(strtmp); i<20; i++)
  {
    strtmp[i]=' ';
  }
  lcd.print(strtmp);
}
