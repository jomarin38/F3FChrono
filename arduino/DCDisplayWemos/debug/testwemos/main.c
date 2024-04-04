#include <stdio.h>
#include <string.h>

void displaySendDataFromServer(const char *str);
void getLineInString(char *initialStr, char **ptrfind);
int getLineInfo(char *initialStr, char **ptrtarget, char **ptrcmd, char **ptrlinenb, char **ptrdata);
void displaySendClear(void);
void displaySendLine (char *nbline, char*data);

int main()
{
    //char str[200]="DISPLAY:CLEAR:\nDISPLAY:line:0:DC Display\nDISPLAY:line:2:AWAITING CONTEST\nDISPLAY:line:3:192.168.1.10\nDISPLAY:line:1: -1  -1.0m/s Init\n";
    char str[200]="DISPLAY:line:1: -1  -1.0m/s Init\n";
    printf("Hello World!\n");
    displaySendDataFromServer(str);
    return 0;
}

void displaySendDataFromServer(const char *str)
{
  char initialStr[200];
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
      ptrtarget=NULL;ptrcmd=NULL;ptrnbline=NULL;ptrdata=NULL;
      tmp = getLineInfo(ptrinprocess, &ptrtarget, &ptrcmd, &ptrnbline, &ptrdata);
      if (tmp==0){
          //printf("cmd : %s, nbline : %s, data : %s\n\n", ptrcmd, ptrnbline, ptrdata);
          //Process command
          if (strcmp(ptrtarget, "DISPLAY")==0 && strcmp(ptrcmd, "CLEAR")==0){
            displaySendClear();
          }
          if (strcmp(ptrtarget, "DISPLAY")==0 && strcmp(ptrcmd, "line")==0 && ptrnbline!=NULL && ptrdata!=NULL){
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

void displaySendClear(void)
{
    printf("display send clear\n");
}

void displaySendLine (char *nbline, char*data)
{
    printf("display line:%s, data:%-20s\n", nbline, data);
}
