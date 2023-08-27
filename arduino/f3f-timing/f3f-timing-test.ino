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

/*
  F3F Timing test 
  Generate output 5 & 6 to simulate base A & B
*/
#include <Wire.h>

const unsigned long BASEONTIME = 100;
const unsigned long BASEOFFTIME = 1900;
const byte TEST_APIN = 5;
const byte TEST_BPIN = 6;

volatile byte outputBase = LOW;
volatile byte currentbase = TEST_APIN;
volatile unsigned long roundCounter = 0;
volatile unsigned long countTimer = 0;

void test_setup(void){
  pinMode (TEST_APIN, OUTPUT);  
  digitalWrite (TEST_APIN, LOW);
  pinMode (TEST_BPIN, OUTPUT);  
  digitalWrite (TEST_BPIN, LOW);
  roundCounter = 0;
}

void test_run(unsigned int delay){
    if (chronostatus.runStatus==Finished){
      roundCounter++;
      Serial.print("round counter : ");
      Serial.println(roundCounter);  
    }
    if (chronostatus.runStatus==InWait or chronostatus.runStatus==Finished){
      chronostatus.runStatus=Launched;
      memset(&chrono, 0, sizeof(chrono));
      chronostart(startLaunched);
      printresetchrono();
      printchrono();
      printclimbout_time();
    }
  
    if (outputBase==HIGH){
      if (countTimer>BASEONTIME){
        outputBase = LOW;
        digitalWrite(currentbase, outputBase);
        countTimer = 0;
      }
    }else{
      if (countTimer>BASEOFFTIME){
        outputBase = HIGH;
        if (currentbase==TEST_APIN){
          if (chronostatus.runStatus>InStart_Late){
            currentbase=TEST_BPIN;
          }
        }else{
          currentbase=TEST_APIN;
        }
        digitalWrite(currentbase, outputBase);
        countTimer = 0;
      }
    }
    countTimer+=delay;
}
