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

const int REBUNDTIME = 500;

typedef struct {
  unsigned long old_event;
  unsigned long rebundBtn_time;
  unsigned long nbInterrupt;
  byte Pin;
  byte Attach;
} baseEventStr;

volatile baseEventStr baseA = {0}, baseB = {0};

void base_setup(void){
  memset (&baseA, 0, sizeof(baseA));
  baseA.rebundBtn_time = REBUNDTIME;
  baseA.Pin = BASEAPIN;

  memset (&baseB, 0, sizeof(baseB));
  baseB.rebundBtn_time = REBUNDTIME;
  baseB.Pin = BASEBPIN;
  //Initialize buttons pin in interrupt mode
  pinMode(baseA.Pin, INPUT_PULLUP);
  baseAttach(baseA.Pin);
  pinMode(baseB.Pin, INPUT_PULLUP);
  baseAttach(baseB.Pin);
}

void baseA_Interrupt(void) {
  //Serial.println("interrupt");
  if ((baseA.old_event + baseA.rebundBtn_time) < millis()) {
    if (digitalRead(baseA.Pin)==LOW){
      //Serial.println("LOW");
      baseCheck(baseA.Pin);
      baseA.old_event=millis();
      baseA.nbInterrupt++;
      baseDetach(baseA.Pin);
    }
  }
}

void baseA_check(void){
  if (baseA.Attach==false){
    if (digitalRead(baseA.Pin)==LOW){
      baseA.old_event=millis();
      //Serial.println("LOW"); 
    }else{
      //Serial.println("HIGH");
      if ((baseA.old_event + baseA.rebundBtn_time) < millis()){
        baseAttach(baseA.Pin);
      }
    }
  }
}

void baseB_Interrupt(void) {
  if ((baseB.old_event + baseB.rebundBtn_time) < millis()) {
    if (digitalRead(baseB.Pin)==LOW){
      baseCheck(baseB.Pin);
      baseB.old_event=millis();
      baseB.nbInterrupt++;
      baseDetach(baseB.Pin);
    }
  }
}

void baseB_check(void){
  if (baseB.Attach==false){
    if (digitalRead(baseB.Pin)==LOW){
      baseA.old_event=millis();
      //Serial.println("LOW"); 
    }else{
      //Serial.println("HIGH");
      if ((baseB.old_event + baseB.rebundBtn_time) < millis()){
        baseAttach(baseB.Pin);
      }
    }
  }
}

void baseAttach(int pin){
  //Serial.println("AttachInterrupt");
  if (pin==baseA.Pin){
    attachInterrupt(digitalPinToInterrupt(baseA.Pin), baseA_Interrupt, FALLING);
    baseA.Attach=true;
  }
  if (pin==baseB.Pin){
    attachInterrupt(digitalPinToInterrupt(baseB.Pin), baseB_Interrupt, FALLING);    
    baseB.Attach=true;
  }
}

void baseDetach(int pin){
  //Serial.println("DetachInterrupt");
  
  if (pin==baseA.Pin){
    detachInterrupt(digitalPinToInterrupt(baseA.Pin));
    baseA.Attach=false;
  }
  if (pin==baseB.Pin){
    detachInterrupt(digitalPinToInterrupt(baseB.Pin));
    baseB.Attach=false;
  }

}

void printbase(void){
  Serial.print("baseA,");
  Serial.print("rebundtime,");
  Serial.print(baseA.rebundBtn_time);
  Serial.print(",nbinterrrupt,");
  Serial.print(baseA.nbInterrupt);
  Serial.print(",baseB");
  Serial.print(",rebundtime,");
  Serial.print(baseA.rebundBtn_time);
  Serial.print(",nbinterrrupt,");
  Serial.print(baseB.nbInterrupt);
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
