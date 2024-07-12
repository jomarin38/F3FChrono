 /** 
 # This file is part of the F3FPicametre distribution (https://github.com/jomarin38/F3FChrono).
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

#define DISPLAY_CLEAR "D:C:"
#define DISPLAY_TIME  "D:T:"
void display_Start(void)
{
  DebugStr(DEBUG_START, DEBUG_LN, "display Module Start");
  displaySendClear();
  displaySendTime("88.88");
}

void displaySendClear(void)
{
  char localstr[60];
  
  strcpy(localstr, DISPLAY_CLEAR);
  msgWrite(localstr);  
  serial_run();
  //Serial.println(localstr);
}


void displaySendAwaitingWifi(char * str)
{
  char msg[20];
  float accu;
  
  Analog_getVoltage(&accu);
  sprintf(msg, "%05.2f", accu);
  displaySendTime(msg);
  serial_run();
}

void display_sendWifiConnected(const char *str)
{
  char msg[20];
  
  displaySendTime(str);
}

void displaySendTime(const char *str)
{
  char localstr[60];
    
  strcpy(localstr, DISPLAY_TIME);
  strcat(localstr, str);
  strcat(localstr, ":");
  msgWrite(localstr);  
}

void displaySendDataFromServer(const char *str)
{
  char initialStr[1024];
  char *ptrline;
  char *ptrinprocess;
  char *ptrtarget;
  char *ptrcmd;
  char *ptrdata;
  int tmp;
  
  strcpy (initialStr, str);
  getLineInString(initialStr, &ptrline);
  ptrinprocess = initialStr;
  while(ptrline!=NULL){
      *ptrline='\0';
      tmp = getLineInfo(ptrinprocess, &ptrtarget, &ptrcmd, &ptrdata);
      if (tmp==0){
          /*Serial.print(ptrtarget);
          Serial.print(", cmd:");
          Serial.print(ptrcmd);
          Serial.print(", nbline:");
          Serial.print(ptrnbline);
          Serial.print(", data:");
          Serial.print(ptrdata);
          Serial.print(" cmpresult:");
          Serial.println((strcmp(ptrtarget, "DISPLAY")==0));// and strcmp(ptrcmd, "line")==0 and ptrnbline!=NULL and ptrdata!=NULL));
          */
          //Process command
          if (strcmp(ptrtarget, "DISPLAY")==0 and strcmp(ptrcmd, "CLEAR")==0){
            displaySendClear();
          }
          if (strcmp(ptrtarget, "DISPLAY")==0 and strcmp(ptrcmd, "TIME")==0 and ptrdata!=NULL){
            displaySendTime(ptrdata);
          }
      }
      ptrinprocess = &initialStr[ptrline-initialStr+1];
      getLineInString(ptrinprocess, &ptrline);
      //ptr = NULL;
  }  
  //DebugStr(DEBUG_START, DEBUG_LN, "end displaySendDataFromServer");
}

void getLineInString(char *initialStr, char **ptrfind)
{
  *ptrfind = strchr(initialStr, '\n');
}

int getLineInfo(char *initialStr, char **ptrtarget, char **ptrcmd, char **ptrdata)
{
  int status = -1;
  char *ptrstr;
  char *ptrsearch;
  char *ptrline;

  *ptrcmd = NULL;
  *ptrdata = NULL;

  ptrstr=initialStr;
  ptrsearch = strchr (ptrstr,':');
  if (ptrsearch!=NULL){
      *ptrsearch='\0';
      *ptrtarget = ptrstr;
      ptrstr = ptrsearch+1;
      ptrsearch = strchr (ptrstr,':');
      if (ptrsearch!=NULL){
          *ptrcmd = ptrstr;
          *ptrsearch='\0';
          *ptrdata = ptrsearch+1;
          status = 0;
      }
  }
  //printf("cmd : %s, nbline : %s, data : %s\n\n", *ptrcmd, *ptrlinenb, *ptrdata);
  return status;
}
