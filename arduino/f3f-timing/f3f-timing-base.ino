 /** 
 # This file is part of the F3FChrono distribution (https://github.com/jomarin38/F3FChrono).
 # Copyright (c) 2021 Sylvain DAVIET, Joel MARIN.
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

const byte BASEAPIN = 2;
const byte BASEBPIN = 3;
const byte BTNNEXTPIN = -1; //Not a real btn

const int REBUNDTIME = 80;

typedef struct {
  unsigned long old_event;
  unsigned long rebundBtn_time;
  unsigned long nbInterrupt;
  byte Pin;
  byte Attach;
} baseEventStr;

volatile baseEventStr baseA = {0}, baseB = {0};
volatile byte baseDebug = false;


void base_setup(void){
  memset (&baseA, 0, sizeof(baseA));
  baseA.rebundBtn_time = REBUNDTIME;
  baseA.Pin = BASEAPIN;

  memset (&baseB, 0, sizeof(baseB));
  baseB.rebundBtn_time = REBUNDTIME;
  baseB.Pin = BASEBPIN;
  //Initialize buttons pin in interrupt mode
  pinMode(baseA.Pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(baseA.Pin), baseA_Interrupt, FALLING);
  baseA.Attach=true;
  pinMode(baseB.Pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(baseB.Pin), baseB_Interrupt, FALLING);    
  baseB.Attach=true;
}

void baseA_Interrupt(void) {
  baseA.old_event=millis();
  if (baseA.Attach==true){
    baseCheck(baseA.Pin);
  }
  baseA.Attach=false;
  baseA.nbInterrupt++;
}

void baseA_check(void){
  if (baseA.Attach==false){
    if (digitalRead(baseA.Pin)==LOW){
      baseA.old_event=millis(); 
    }else{
      if ((baseA.old_event + baseA.rebundBtn_time) < millis()){
        baseA.Attach=true;
        if (baseDebug==true){
          printbaseA();
        }
      }
    }
  }
}

void baseB_Interrupt(void) {
  if (baseB.Attach==true){
    baseCheck(baseB.Pin);
  }
  baseB.Attach=false;
  baseB.old_event=millis();
  baseB.nbInterrupt++;
}

void baseB_check(void){
  if (baseB.Attach==false){
    if (digitalRead(baseB.Pin)==LOW){
      baseB.old_event=millis();
    }else{
      if ((baseB.old_event + baseB.rebundBtn_time) < millis()){
        baseB.Attach=true;
        if (baseDebug==true){
          printbaseB();  
        }
      }
    }
  }
}


void printbaseA(void){
  Serial.print("baseA,");
  Serial.print("rebundtime,");
  Serial.print(baseA.rebundBtn_time);
  Serial.print(",nbinterrrupt,");
  Serial.print(baseA.nbInterrupt);
  Serial.print(",attach?");
  Serial.print(baseA.Attach);
  Serial.print(",calcrebound:");
  Serial.print(baseA.old_event + baseA.rebundBtn_time);
  Serial.print(",millis():");
  Serial.print(millis());
  Serial.println(",");
}
void printbaseB(void){
  Serial.print("baseB");
  Serial.print(",rebundtime,");
  Serial.print(baseB.rebundBtn_time);
  Serial.print(",nbinterrrupt,");
  Serial.print(baseB.nbInterrupt);
  Serial.print(",attach?");
  Serial.print(baseB.Attach);
  Serial.print(",calc rebound:");
  Serial.print(baseB.old_event + baseB.rebundBtn_time);
  Serial.print(",millis()");
  Serial.print(millis());
  Serial.println(",");
}


void printforcebaseA(void){
  Serial.print("force baseA");
  Serial.println(",");
}

void printforcebaseB(void){
  Serial.print("force baseB");
  Serial.println(",");
}

void printforcebtnnext(void){
  Serial.print("force btn next");
  Serial.println(",");
}
