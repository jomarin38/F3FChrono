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

#define DISPLAY_SEP "DISP:"
#define DISPLAY     "DISP"
#define CLEAR       "CLEAR"
#define LINE        "L"
#define MAX_DATA    256

typedef struct{
  char data_read[MAX_DATA];
  byte nb_data;
  byte data_available;
}serialStr;

volatile serialStr serial;


void serial_setup(void){
  memset (&serial,0, sizeof(serial));
  //Serial.begin(57600);
  Serial.begin(19200);
  while (!Serial) {
    delay(100);  
  }
  Serial.setTimeout(100);
  DebugStr(DEBUG_START, DEBUG_NOLN, "DCDisplay,setup,version : ");
  DebugStr(DEBUG_START, DEBUG_LN, VERSION);


}

void serial_run(void) {
  char *ptrfind=NULL;
  char *ptrdisplay=NULL;
  char *ptrcmd=NULL;
  char *ptrline=NULL;
  char *ptrmsg=NULL;
  int line=0;
 
  //Process serial request
  
  if (serial.data_available) {
    Serial.println("Processing Data");
    ptrdisplay = &serial.data_read[0];
    ptrfind = strstr(ptrdisplay, DISPLAY_SEP);
    while(ptrfind!=NULL){
      ptrcmd = ptrfind + strlen(DISPLAY_SEP);
      *(ptrcmd-1)='\0';
      DebugStr(DEBUG_START, DEBUG_NOLN, "found display ?");
      DebugStr(DEBUG_NOSTART, DEBUG_LN, ptrfind);
      printf ("strcmp (DISPLAY) ? %d\n", strcmp(ptrfind, "DISPLAY"));
      if (strcmp(ptrfind, DISPLAY)==0){
        ptrfind = strstr(ptrcmd, ":");
        *ptrfind='\0';
        DebugStr(DEBUG_START, DEBUG_NOLN, "found cmd ?");
        DebugStr(DEBUG_NOSTART, DEBUG_LN, ptrcmd);
        if (strcmp(ptrcmd, CLEAR)==0){
          DebugStr(DEBUG_START, DEBUG_LN, "DisplayClear()");
          //displayClear();
        }else{
          ptrline = ptrfind +1;
          if (strcmp(ptrcmd, LINE)==0){
            ptrfind = strstr(ptrline, ":");
            ptrmsg = ptrfind +1;
            *ptrfind='\0';
            ptrfind=strstr(ptrmsg,":");
            if (ptrfind){
              *ptrfind='\0';
            }
            DebugStr(DEBUG_START, DEBUG_LN, ptrline);
            DebugStr(DEBUG_START, DEBUG_LN, ptrmsg);
            DebugStr(DEBUG_START, DEBUG_LN, "Displayline()");
            displayPrintLine(atoi(ptrline), ptrmsg);
          }
        }
      }
      ptrdisplay=ptrfind+1;
      ptrfind = strstr(ptrdisplay, DISPLAY_SEP);
      printf("new string : %s\n\n", ptrdisplay);
    }
    memset(&serial, 0, sizeof(serial));
    Serial.println("memset serialData");
  }
}


void serial_read(){
  int i;
  
  if (Serial.available()>0 && serial.data_available==false){
    Serial.println("");
    Serial.print("Data read : ");
//    while (Serial.available()>0 && serial.data_available==false){
    while (serial.data_available==false){
      i = Serial.readBytes((char*)&serial.data_read[serial.nb_data], 1);
      if (i>0){
        Serial.print(serial.data_read[serial.nb_data]);
        if (serial.data_read[serial.nb_data]=='\x0A'){
          serial.data_available=true;
          Serial.println(serial.nb_data);
        }else{
          serial.nb_data+=1;
        }
      }else{
        Serial.println("");
        Serial.println(serial.nb_data);
        serial.data_available = (serial.nb_data>0);
      }
    }
/*    if (serial.nb_data>0 && !serial.data_available){
      Serial.println("");
      serial.data_available=true;
      Serial.println(serial.nb_data);
    }*/
  }
}
/*void serialEvent(){
  if (serial.data_available==false){
    serial.nb_data = Serial.readBytesUntil('\x0a', (char*)serial.data_read, 256);
    if (serial.nb_data>0){
      serial.data_read[serial.nb_data+1]='\0';
      serial.nb_data+=1;
      serial.data_available=true;
      Serial.println("");
      Serial.print("Data read : ");
      Serial.println(serial.nb_data);
      
      Serial.println((char*)serial.data_read);
    }
  }
/*    
 *  if (serial.nb_data<sizeof (serial.data_read)/sizeof(char)-1){
      serial.nb_data++;        
    }else{
      serial.nb_data=0;
      Serial.println("");
      Serial.println("Max Data");
    }
  }
  
      
}*/
