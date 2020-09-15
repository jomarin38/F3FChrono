typedef struct{
  char data_read[10];
  byte nb_data;
  byte data_available;
}serialStr;

volatile serialStr serial;


void serial_setup(void){
  memset (&serial,0, sizeof(serial));
  Serial.begin(57600);
  while (!Serial) {
    delay(100);  
  }
  Serial.print("F3FChrono,setup,version : ");
  Serial.println(VERSION);

}

void serial_run(void) {
  if (reset){
    reset=false;
    printreset();
  }
  //check if status changed
  temp = memcmp (&chronostatus, &chronostatus_old, sizeof(chronostatus));
  if (temp != 0){
    printstatus();
    memcpy(&chronostatus_old, &chronostatus, sizeof(chronostatus));
  }
  //check if lap changed
  temp = memcmp (&chrono, &chrono_old, sizeof(chrono));
  if (temp != 0){
    memcpy(&chrono_old, &chrono, sizeof(chrono));
    printchrono();
  }
  
  //Process serial request
  if (serial.data_available) {
    char tmp = serial.data_read[0];
    if (tmp=='t'){ //Set buzzer time
      buzzer.Time=0;
      for (i=1; i<serial.nb_data-1; i++){
        buzzer.Time = buzzer.Time*10+(int)(serial.data_read[i]-'0');
      }
      led.Time = buzzer.Time;
      printbuzzer();
    }else if (tmp=='d'){  //debug
      printdebug();
    }else if (tmp=='s'){  //Start chrono
      chronostatus.runStatus=byte(serial.data_read[1]-'0');
      if (chronostatus.runStatus==Launched) {
        chronostart(startLaunched);
        buzzerSet(1);
      }
      printstatus();
    }else if (tmp=='b'){  //set base rebound time
      baseA.rebundBtn_time=0;
      for (i=1; i<serial.nb_data-1; i++){
        baseA.rebundBtn_time = baseA.rebundBtn_time*10+(int)(serial.data_read[i]-'0');
      }
      baseB.rebundBtn_time = baseA.rebundBtn_time;
      printbase();
    }else if (tmp=='v'){  //Send voltage
      printvoltage();
    }else if (tmp=='r'){  //Reset chrono
      memset(&chronostatus, 0, sizeof(chronostatus));
      memset(&chrono, 0, sizeof(chrono));
      printresetchrono();
    }else if (tmp=='e'){  //event base or btn next
      if (serial.data_read[1]=='a'){
        baseCheck(baseA.Pin);
        printforcebaseA();
      }else if (serial.data_read[1]=='b'){
        baseCheck(baseB.Pin);
        printforcebaseB();
      }else if (serial.data_read[1]=='n'){
        baseCheck(BTNNEXTPIN);
        printforcebtnnext();
      }
    }else if (tmp=='k'){  //reboot arduino
      resetFunc();
    }else if (tmp=='m'){  //Set chrono mode
      chrono_mode = serial.data_read[1]-'0';
      printmode();
      if (chrono_mode==Training){
        memset(&chronostatus, 0, sizeof(chronostatus));
        memset(&chrono, 0, sizeof(chrono));
        chronostatus.runStatus=InStart;        
      }
      if (chrono_mode==Race){
        memset(&chronostatus, 0, sizeof(chronostatus));
        memset(&chrono, 0, sizeof(chrono));
      }
    }
    
    
    memset(&serial, 0, sizeof(serial));
  }
  //buzzerRun(&led);
}

void serialEvent(){
  while (Serial.available()){
    if (serial.data_available==false){
      serial.data_read[serial.nb_data]=(char)Serial.read();
      if (serial.data_read[serial.nb_data]=='\n'){
        serial.data_available=true;
      }
      if (serial.nb_data<sizeof (serial.data_read)/sizeof(char)){
        serial.nb_data++;        
      }else{
        serial.nb_data=0;
      }
    }
        
  }  
}

void printdebug(void){
  printmode();
  printstatus();
  printchrono();
  printbase();
  printvoltage();
  printoutput();
}
