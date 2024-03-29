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

volatile buzzerStr buzzer = {0};
volatile buzzerStr led = {0};

void output_setup(void){
  memset (&buzzer, 0, sizeof(buzzer));
  memset (&led, 0, sizeof(led));
  buzzer.Time = BUZZERTIME;
  buzzer.Pin = BUZZERPIN;

  led.Time = LEDTIME;
  led.Pin = LED_BUILTIN;
  // initialize digital pin LED_BUILTIN and buzzer PIN as an output.
  pinMode(buzzer.Pin, OUTPUT);
  pinMode(led.Pin, OUTPUT);
}

void buzzerRun(void) {
  if (buzzer.Cmd != 0) {
    if (buzzer.State == true and buzzer.Count <= buzzer.Time) {
      digitalWrite(buzzer.Pin, HIGH);
      buzzer.Count += LOOPDELAY;
      if (buzzer.Count >= buzzer.Time) {
        buzzer.State = false;
        buzzer.Count = 0;
      }
    }
    if (buzzer.State == false and buzzer.Count <= buzzer.Time) {
      digitalWrite(buzzer.Pin, LOW);
      buzzer.Count += LOOPDELAY;
      if (buzzer.Count >= buzzer.Time) {
        buzzer.State = false;
        buzzer.Count = 0;
        if (buzzer.Cmd != 0) {
          if (buzzer.Cmd > 0) {
            buzzer.Cmd -= 1;
          }
          buzzer.State = true;
        }
      }
    }
  }
}

void buzzerSet(byte nb)
{
  if (buzzer.Cmd==0){
    buzzer.Cmd=nb;
    buzzer.State=true;
  }
}

void buzzer_lowlevel(int state){
  Serial.print("buzzer lowlevel,");
  Serial.print(state);
  Serial.print(", pin : ");
  Serial.println(BUZZERPIN);
  
  if (state){
    digitalWrite(BUZZERPIN, HIGH);
  }else{
    digitalWrite(BUZZERPIN, LOW);
  }
}


void printbuzzer(void){
  Serial.print("buzzertime,");
  Serial.print(buzzer.Time);
  Serial.println(",");
}

void printoutput(void){
  led.Cmd = -1;
  Serial.print("buzzer,");
  Serial.print("cmd,");
  Serial.print(buzzer.Cmd);
  Serial.print(",time,");
  Serial.print(buzzer.Time);
  Serial.print(",state,");
  Serial.print(buzzer.State);
  Serial.print(",pin,");
  Serial.print(buzzer.Pin);
  Serial.print(",led,");
  Serial.print("cmd,");
  Serial.print(led.Cmd);
  Serial.print(",time,");
  Serial.print(led.Time);
  Serial.print(",state,");
  Serial.print(led.State);
  Serial.println(",");
}
