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

#define DISPLAY_SEP     "D:"
#define DISPLAY         "D"
#define CLEAR           "C"
#define LINE            "L"
#define SERIAL_MAX_DATA 256
#define MSG_MAX_LEN     60
#define MSG_MAX_BUFFER  5

typedef struct{
  char data_read[SERIAL_MAX_DATA];
  byte nb_data;
}serialStr;

typedef struct{
  char msg[MSG_MAX_BUFFER][MSG_MAX_LEN];
  char id_read;
  char id_write;
}serialmsgStr;

volatile serialStr serial;
static serialmsgStr msgbuffer;

void serial_setup(void){
  memset (&serial, 0, sizeof(serial));
  memset (&msgbuffer, 0, sizeof(serialmsgStr));
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
  char *ptrinprocess;
  char *ptrtarget;
  char *ptrcmd;
  char *ptrnbline;
  char *ptrdata;
  int tmp;
  char localmsg[MSG_MAX_LEN];
  int line=0;
 
  //Process serial request
  if (msgAvailable()>0) {
    DebugStr(DEBUG_START, DEBUG_LN, "msgAvailable()?true");
    if (msgRead(localmsg)>=0){
      ptrinprocess = localmsg;
      tmp = getLineInfo(ptrinprocess, &ptrtarget, &ptrcmd, &ptrnbline, &ptrdata);
      if (tmp==0){
          DebugStr(DEBUG_START, DEBUG_NOLN, ptrtarget);
          DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ", cmd:");
          DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ptrcmd);
          DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ", nbline:");
          DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ptrnbline);
          DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ", data:");
          DebugStr(DEBUG_NOSTART, DEBUG_LN, ptrdata);

        //Process command
        if (strcmp(ptrtarget, DISPLAY)==0 and strcmp(ptrcmd, CLEAR)==0){
          displayClear();
        }
        if (strcmp(ptrtarget, DISPLAY)==0 and strcmp(ptrcmd, LINE)==0 and ptrnbline!=NULL and ptrdata!=NULL){
          displayPrintLine(atoi(ptrnbline), ptrdata);
        }  
      }  
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

  ptrfind = strstr(data, DISPLAY_SEP);
  if(ptrfind!=NULL){
    if (strlen(ptrfind)<MSG_MAX_LEN){
      strcpy(&msgbuffer.msg[msgbuffer.id_write][0], ptrfind);
      msgbuffer.id_write = (msgbuffer.id_write+1)%MSG_MAX_BUFFER;
      DebugStr(DEBUG_START, DEBUG_NOLN, "msgWrite(), id_write : ");
      sprintf(localstr, "%d", msgbuffer.id_write);
      DebugStr(DEBUG_NOSTART, DEBUG_LN, localstr);
    }else{
      DebugStr(DEBUG_START, DEBUG_LN,"buffer len is too high for msg buffer");
    }
  }
}

void serialEvent(){
  int i;
  int nbdata;
  char localstr[SERIAL_RX_BUFFER_SIZE];
  char *ptrfind;
  
  if ((Serial.available()+serial.nb_data)>SERIAL_MAX_DATA){
    DebugStr(DEBUG_START, DEBUG_LN,"RAZ serial data buffer full no end caracter found");
    memset(&serial, 0, sizeof(serial));
  }
  nbdata = Serial.readBytes((char*)localstr, Serial.available());
  if (nbdata>0){
      /*Serial.print("Serial receive : ");
      Serial.println(nbdata);
      */
    for (i=0; i<nbdata; i++){
      /*if (localstr[i]>=0x20 & localstr[i]<0x7F){
        Serial.print(localstr[i]);
      }else{Serial.print(localstr[i], HEX);}
      */
      serial.data_read[serial.nb_data]=localstr[i];
      serial.nb_data++;
      if (localstr[i]==0x0A){
        /*Serial.println();
        Serial.print("Serial add to msfbuffer : ");
        Serial.println((char*)serial.data_read);
        */
        msgWrite(serial.data_read);
        Serial.println("1");
        memset(&serial, 0, sizeof(serial));
      }  
    }
    //if buffer full and no end caracter find, trash data...
    if (serial.nb_data>=SERIAL_MAX_DATA){
      //Serial.println("Serial max buffer size before 0x0A");
      memset(&serial, 0, sizeof(serial));
    }
  }
}

int getLineInfo(char *initialStr, char **ptrtarget, char **ptrcmd, char **ptrlinenb, char **ptrdata)
{
  int status = -1;
  char *ptrstr;
  char *ptrsearch;

  *ptrcmd = NULL;
  *ptrlinenb = NULL;
  *ptrdata = NULL;

  ptrstr=initialStr;
  ptrsearch = strchr (ptrstr,':');
  if (ptrsearch!=NULL){
    *ptrsearch=0x0;
    *ptrtarget = ptrstr;
    ptrstr = ptrsearch+1;
    ptrsearch = strchr (ptrstr,':');
    if (ptrsearch!=NULL){
      *ptrsearch=0x0;
      *ptrcmd = ptrstr;
      ptrstr = ptrsearch+1;
      ptrsearch = strchr (ptrstr,':');
      if (ptrsearch!=NULL){
        *ptrsearch=0x0;
        *ptrlinenb = ptrstr;
        ptrstr = ptrsearch+1;
        ptrsearch = strchr (ptrstr,':');
        DebugStr(DEBUG_START, DEBUG_NOLN,"getlineinfo ptrmsg : ");
        DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ptrstr);
        DebugStr(DEBUG_NOSTART, DEBUG_NOLN, ", find : ");
        DebugStr(DEBUG_NOSTART, DEBUG_LN, ptrsearch);
        if (ptrsearch!=NULL){
          *ptrsearch=0x0;
          *ptrdata = ptrstr;
        }
      }
      status = 0;
    }
  }
  //printf("cmd : %s, nbline : %s, data : %s\n\n", *ptrcmd, *ptrlinenb, *ptrdata);
  return status;
}
