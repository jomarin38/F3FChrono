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
  displayPrintLine(0, "DC Display");
  displayPrintLine(1, "Test line 1");
  displayPrintLine(2, "Test line 2");
  displayPrintLine(3, "Test line 3");
}

void displayClear(void)
{
  lcd.clear();
}

void displayPrintLine(int line, char *str)
{
  lcd.setCursor(0, line);
  lcd.print(str);
}
