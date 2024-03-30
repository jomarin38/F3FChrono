#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define _DEBUG_
#define DEBUG_LN true
#define DEBUG_NOLN false
#define DEBUG_START true
#define DEBUG_NOSTART false
#ifdef _DEBUG_
  static void DebugStr(bool debug, bool ln, const char *str)
  {
    if (debug){
      printf("DEBUG - ");
    }
    if (ln){
      printf("%s\n", str);  
    }else{
      printf("%s", str);  
    }
  }
#else
  static void DebugStr(bool debug, bool ln, const char *str)
  {
    str;
  }
 #endif
 
 #define MAX_DATA 256
 #define byte unsigned char
typedef struct{
  char data_read[MAX_DATA];
  byte nb_data;
  byte data_available;
}serialStr;

volatile serialStr serial;

char string[1000]="G⸮Z⸮Q`@dI⸮⸮*ߝhF⸮W⸮TWZI-DTG⸮V`\	dH`H5lJ⸮P@wdJ⸮DW⸮`\⸮⸮d`\⸮*`PP@⸮`HX⸮p⸮Le⸮U&`\B0Q&`\B`Z`H⸮DLDZ⸮X⸮Qچ⸮dHD*M(+ną%DF%dVh@`:\nDISPLAY:CLEAR:\nDISPLAY:LINE:0:DC&JUDGE DISPLAY\nDISPLAY:LINE:2:AWAITING WIFI\n";

void serial_run(void);
int main (void)
{
	strcpy((char*)serial.data_read, string);
	serial.data_available = true;
	printf("data on buffer : %s\nStart processing ---\n\n",serial.data_read);
	serial_run();
	return 0;
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
  
    ptrdisplay = &serial.data_read[0];
    ptrfind = strstr(ptrdisplay, "DISPLAY:");
    while(ptrfind!=NULL){
	    ptrcmd = ptrfind + strlen("DISPLAY:");
	    *(ptrcmd-1)='\0';
	    //if (ptrfind){
	      DebugStr(DEBUG_START, DEBUG_LN, ptrfind);
	      printf ("strcmp (DISPLAY) ? %d\n", strcmp(ptrfind, "DISPLAY"));
	      if (strcmp(ptrfind, "DISPLAY")==0){
		ptrfind = strstr(ptrcmd, ":");
		*ptrfind='\0';
	        DebugStr(DEBUG_START, DEBUG_LN, ptrcmd);
		if (strcmp(ptrcmd, "CLEAR")==0){
		  printf("displayClear()\n");
		  //displayClear();
		}else{
		  ptrline = ptrfind +1;
		  if (strcmp(ptrcmd, "LINE")==0){
		    ptrfind = strstr(ptrline, ":");
		    ptrmsg = ptrfind +1;
		    *ptrfind='\0';
		    ptrfind=strstr(ptrmsg,"\n");
		    if (ptrfind){
			*ptrfind='\0';
		        DebugStr(DEBUG_START, DEBUG_LN, ptrline);
			DebugStr(DEBUG_START, DEBUG_LN, ptrmsg);
			printf("displayPrintLine()\n");
			//displayPrintLine(atoi(ptrline), ptrmsg);
		    }
		  }
		}
	      }
	    //}
	    ptrdisplay=ptrfind+1;
	    ptrfind = strstr(ptrdisplay, "DISPLAY:");
	    printf("new string : %s\n\n", ptrdisplay);
	}
	memset((void*)&serial, 0, sizeof(serial));
  }
}
