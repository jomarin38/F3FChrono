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
#define SERIAL_MAX_DATA 256
#define MSG_MAX_LEN     40
#define MSG_MAX_BUFFER  8

typedef enum{
  readytosend=0,
  awaiting_ack=1
}serialState;

typedef struct{
  serialState state;
}serialStr;

typedef struct{
  char msg[MSG_MAX_BUFFER][MSG_MAX_LEN];
  char id_read;
  char id_write;
}serialmsgStr;

serialStr serial;
serialmsgStr msgbuffer;

void serial_setup(void){
  memset (&serial, 0, sizeof(serial));
  memset (&msgbuffer, 0, sizeof(serialmsgStr));
  //Serial.begin(57600);
  Serial.begin(19200);
  while (!Serial) {
    delay(100);  
  }
  Serial.flush();
  Serial.setTimeout(100);
  delay(100);
  Serial.println();
  Serial.println();
  serial.state=readytosend;
  DebugStr(DEBUG_START, DEBUG_NOLN, "DCDisplayWemos,setup,version : ");
  DebugStr(DEBUG_START, DEBUG_LN, VERSION);
}

void serial_run(void) {
  char localmsg[MSG_MAX_LEN];


  //Process serial request
  if (serial.state == readytosend & msgAvailable()>0) {
    DebugStr(DEBUG_START, DEBUG_LN, "msgAvailable()?true");
    if (msgRead(localmsg)>=0){
      Serial.println(localmsg);
      serial.state = awaiting_ack;
    }
  }
}

int msgAvailable(){
  int ret;
  if (msgbuffer.id_write>=msgbuffer.id_read){
    ret = msgbuffer.id_write-msgbuffer.id_read;
  }else{
    ret = MSG_MAX_BUFFER - msgbuffer.id_read + msgbuffer.id_write;
  }
  return ret;
}

int msgRead(char *ptrmsg)
{
  int ret=0;
  char localstr[10];

  if (ptrmsg!=NULL){
    strcpy(ptrmsg, &msgbuffer.msg[msgbuffer.id_read][0]);
    msgbuffer.id_read = (msgbuffer.id_read+1)%MSG_MAX_BUFFER;
    DebugStr(DEBUG_START, DEBUG_NOLN, "msgRead(), index read : ");
    sprintf(localstr, "%d", msgbuffer.id_read);
    DebugStr(DEBUG_NOSTART, DEBUG_LN, localstr);
  }else{
    ret=-1;
  }
  return ret;
}

int msgWrite(char *data){
  int ret;
  char *ptrfind;
  char localstr[10];

  if (strlen(data)<MSG_MAX_LEN){
    strcpy(&msgbuffer.msg[msgbuffer.id_write][0], data);
    msgbuffer.id_write = (msgbuffer.id_write+1)%MSG_MAX_BUFFER;
    DebugStr(DEBUG_START, DEBUG_NOLN, "msgWrite(), id_write : ");
    sprintf(localstr, "%d", msgbuffer.id_write);
    DebugStr(DEBUG_NOSTART, DEBUG_LN, localstr);
  }else{
    DebugStr(DEBUG_START, DEBUG_LN,"buffer len is too high for msg buffer");
  }
  return ret;
}

void serialEvent(){
  int i;
  int nbdata;
  char localstr[100];

  strcpy(localstr, "");
  if (Serial.available()>SERIAL_MAX_DATA){
    DebugStr(DEBUG_START, DEBUG_LN,"RAZ serial data buffer full no end caracter found");
  }
  nbdata = Serial.readBytes((char*)localstr, Serial.available());
  if (nbdata>0){
    DebugStr(DEBUG_START, DEBUG_LN,"Serial data receive :");
    DebugStr(DEBUG_NOSTART, DEBUG_LN,localstr);
    if (localstr[0]=='1'){
      serial.state = readytosend;
    }
  }
}
