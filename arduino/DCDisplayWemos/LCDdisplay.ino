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

#define DISPLAY_CLEAR "DISP:CLEAR:"
#define DISPLAY_LINE  "DISP:L:"
void display_Start(void)
{
  DebugStr(DEBUG_START, DEBUG_LN, "display Module Start");
  displaySendClear();
  displaySendDCJudgeDisplay();
}

void displaySendClear(void)
{
  Serial.println(DISPLAY_CLEAR);
  Serial.flush();
}

void displaySendDCJudgeDisplay(void)
{
  displaySendLine("0", "DC&JUDGE DISPLAY");
}

void displaySendAwaitingWifi(void)
{
  displaySendLine("2", "WIFI ?");
}

void display_sendWifiConnected(const char *str)
{
  displaySendLine("2", "F3FChrono awaiting");
  displaySendLine("3", str);
}

void displaySendLine(const char* linenb, const char *str)
{
  Serial.print(DISPLAY_LINE);
  Serial.print(linenb);
  Serial.print(":");
  Serial.print(str);
  Serial.println(":");
  Serial.flush();
}

void displaySendDataFromServer(const char *str)
{
  char initialStr[1024];
  char *ptrline;
  char *ptrinprocess;
  char *ptrsearch;
  char *ptrtarget;
  char *ptrcmd;
  char *ptrnbline;
  char *ptrdata;
  int tmp;
  
  strcpy (initialStr, str);
  getLineInString(initialStr, &ptrline);
  ptrinprocess = initialStr;
  while(ptrline!=NULL){
      *ptrline='\0';
      tmp = getLineInfo(ptrinprocess, &ptrtarget, &ptrcmd, &ptrnbline, &ptrdata);
      if (tmp==0){
          /*Serial.print(ptrtarget);
          Serial.print(", cmd:");
          Serial.print(ptrcmd);
          Serial.print(", nbline:");
          Serial.print(ptrnbline);
          Serial.print(" data:");
          Serial.print(ptrdata);
          Serial.print(" cmpresult:");
          Serial.println((strcmp(ptrtarget, "DISPLAY")==0));// and strcmp(ptrcmd, "line")==0 and ptrnbline!=NULL and ptrdata!=NULL));
          */
          //Process command
          if (strcmp(ptrtarget, "DISPLAY")==0 and strcmp(ptrcmd, "CLEAR")==0){
            displaySendClear();
          }
          if (strcmp(ptrtarget, "DISPLAY")==0 and strcmp(ptrcmd, "line")==0 and ptrnbline!=NULL and ptrdata!=NULL){
            displaySendLine(ptrnbline, ptrdata);
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

int getLineInfo(char *initialStr, char **ptrtarget, char **ptrcmd, char **ptrlinenb, char **ptrdata)
{
  int status = -1;
  char *ptrstr;
  char *ptrsearch;
  char *ptrline;

  *ptrcmd = NULL;
  *ptrlinenb = NULL;
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
          ptrline = &ptrstr[ptrsearch-ptrstr+1];
          ptrsearch = strchr (ptrline,':');
          if (ptrsearch!=NULL){
              *ptrsearch='\0';
              *ptrlinenb = ptrline;
              *ptrdata = ptrsearch+1;
          }
          status = 0;
      }
  }
  //printf("cmd : %s, nbline : %s, data : %s\n\n", *ptrcmd, *ptrlinenb, *ptrdata);
  return status;
}
