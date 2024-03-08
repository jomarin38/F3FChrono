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


void display_Start(void)
{
  DebugStr(DEBUG_START, DEBUG_LN, "display Module Start");
  displaySendClear();
  displaySendDCDisplay();
  displaySendAwaitingWifi();
}

void displaySendClear(void)
{
  Serial.println("DISPLAY:CLEAR");
}

void displaySendDCDisplay(void)
{
  displaySendLine("1", "DC DISPLAY");
}

void displaySendAwaitingWifi(void)
{
  displaySendLine("2", "AWAITING WIFI");
}

void display_sendWifiConnected(const char *str)
{
  displaySendLine("2", str);
}

void displaySendLine(const char* linenb, const char *str)
{
  Serial.print("DISPLAY:LINE:");
  Serial.print(linenb);
  Serial.print(":");
  Serial.println(str);
}

void displaySendDataFromServer(const char *str)
{
  char initialStr[200];
  char *ptrline;
  char *ptrinprocess;
  char *ptrsearch;
  char *ptrcmd;
  char *ptrnbline;
  char *ptrdata;
  int tmp;
  
  strcpy (initialStr, str);
  getLineInString(initialStr, &ptrline);
  ptrinprocess = initialStr;
  while(ptrline!=NULL){
      *ptrline='\0';
      tmp = getLineInfo(ptrinprocess, &ptrcmd, &ptrnbline, &ptrdata);
      if (tmp==0){
          //printf("cmd : %s, nbline : %s, data : %s\n\n", ptrcmd, ptrnbline, ptrdata);    
          //Process command
          if (strcmp(ptrcmd, "CLEAR")==0){
            displaySendClear();
          }
          if (strcmp(ptrcmd, "line")==0){
            displaySendLine(ptrnbline, ptrdata);
          }
      }
      ptrinprocess = &initialStr[ptrline-initialStr+1];
      getLineInString(ptrinprocess, &ptrline);
      //ptr = NULL;
  }  
}

void getLineInString(char *initialStr, char **ptrfind)
{
  *ptrfind = strchr(initialStr, '\n');
}

int getLineInfo(char *initialStr, char **ptrcmd, char **ptrlinenb, char **ptrdata)
{
  int status = -1;
  char *ptrsearch;
  char *ptrline;
  
  ptrsearch = strchr (initialStr,':');
  if (ptrsearch!=NULL){
      *ptrsearch='\0';
      *ptrcmd = initialStr;
      ptrline = &initialStr[ptrsearch-initialStr+1];
      ptrsearch = strchr (ptrline,':');
      if (ptrsearch!=NULL){
          *ptrsearch='\0';
          *ptrlinenb = ptrline;
          *ptrdata = &initialStr[ptrsearch-initialStr+1];
      }
      status = 0;
  }
  //printf("cmd : %s, nbline : %s, data : %s\n\n", *ptrcmd, *ptrlinenb, *ptrdata);
  return status;
}
