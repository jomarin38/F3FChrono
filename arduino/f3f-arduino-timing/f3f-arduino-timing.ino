/*
  F3F Timing
  use 2 pins as interrupt mode
*/
#include <Wire.h>

#define SLAVE_ADDRESS 0x05
const byte BASEAPIN = 2;
const byte BASEBPIN = 3;
const byte BTNNEXTPIN = -1; //Not a real btn
const byte VOLTAGEPIN = A1;
const byte BUZZERPIN = 12;
const byte LOOPDELAY = 5;
const int BUZZERTIME = 300;
const int LEDTIME = 300;
const int REBUNDTIME = 500;
const int VOLTAGE_TIME = 2000;
const float VERSION = 0.91;

enum chronoStatus {
  InWait = 0,
  WaitLaunch,
  Launched,
  Late,
  InStart,
  InStart_Late,
  InProgressA,
  InProgressB,
  WaitAltitude,
  Finished
};

enum chronoMode{
  Training = 0,
  Race
};

typedef struct {
  byte lapCount;
  byte started;
  unsigned long lap[10];
  unsigned long oldtime;
  unsigned long starttime;
  unsigned long startaltitudetime;
} chronoStr;

typedef struct {
  int runStatus;
}chronoStatusStr;


typedef struct{
  char data_read[10];
  byte nb_data;
  byte data_available;
}serialStr;

typedef struct {
  int Time;     //in milliseconds
  int Count;    //in milliseconds
  int Cmd;      //blink number
  byte State;   //buzzer state
  byte Pin;
} buzzerStr;

typedef struct {
  unsigned long old_event;
  unsigned long rebundBtn_time;
  unsigned long nbInterrupt;
  byte Pin;
} baseEventStr;

typedef struct {
  int readTime;
  int count;
  byte Pin;
  int data[10];
  byte index;
  int sum;
  int rawData;
} analogStr;

typedef struct {
  byte state;
  byte received;
} debugStr;


volatile chronoStr chrono = {0}, chrono_old = {0};
volatile serialStr serial;
volatile chronoStatusStr chronostatus, chronostatus_old;
volatile baseEventStr baseA = {0}, baseB = {0};
volatile analogStr accu = {0};
volatile buzzerStr buzzer = {0};
volatile buzzerStr led = {0};
volatile debugStr debug = {0};
volatile unsigned int i = 0;
volatile byte temp = 0;
volatile byte reset = true;
volatile chronoMode chrono_mode = Training;
/*void baseA_Interrupt(void);
void baseB_Interrupt(void);
void baseCheck(byte base);
void RS232Run(void);
void analogRun(void);
void buzzerRun(buzzerStr *data);
void buzzerSet(buzzerStr *data, byte nb);
void baseCheck(byte base);
*/
void(* resetFunc) (void) = 0;

// the setup function runs once when you press reset or power the board
void setup() {
  //Initialize chrono var.
  memset (&debug, 0, sizeof(debug));
  memset (&chrono, 0, sizeof(chrono));
  memset (&chrono_old, 0, sizeof(chrono_old));
  memset (&chronostatus, 0, sizeof(chronostatus));
  memset (&chronostatus_old, 0, sizeof(chronostatus_old));
  chrono_mode = Training;
  chronostatus.runStatus = InStart;

  memset (&buzzer, 0, sizeof(buzzer));
  memset (&led, 0, sizeof(led));
  memset (&accu, 0, sizeof(accu));
  memset (&serial,0, sizeof(serial));

  buzzer.Time = BUZZERTIME;
  buzzer.Pin = BUZZERPIN;

  led.Time = LEDTIME;
  led.Pin = LED_BUILTIN;

  accu.Pin = VOLTAGEPIN;
  accu.readTime = VOLTAGE_TIME;
  accu.rawData= 900; //Initalize @12V for the first measurements
  
  memset (&baseA, 0, sizeof(baseA));
  baseA.rebundBtn_time = REBUNDTIME;
  baseA.Pin = BASEAPIN;

  memset (&baseB, 0, sizeof(baseB));
  baseB.rebundBtn_time = REBUNDTIME;
  baseB.Pin = BASEBPIN;

  // initialize digital pin LED_BUILTIN and buzzer PIN as an output.
  pinMode(buzzer.Pin, OUTPUT);
  pinMode(led.Pin, OUTPUT);
  //Initialize buttons pin in interrupt mode
  pinMode(baseA.Pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(baseA.Pin), baseA_Interrupt, FALLING);
  pinMode(baseB.Pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(baseB.Pin), baseB_Interrupt, FALLING);

  Serial.begin(57600);
  while (!Serial) {
    delay(100);  
  }
  Serial.print("F3FChrono,setup,version : ");
  Serial.println(VERSION);
}

// the loop function runs over and over again forever
void loop() {
  RS232Run();
  analogRun();
  buzzerRun(&buzzer);
  if (chronostatus.runStatus == WaitAltitude) {
    baseCheck(0);
  }
  delay (LOOPDELAY);
}


void RS232Run(void) {
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
      if (chronostatus.runStatus==InStart_Late or chronostatus.runStatus==Late) {
        chronostart();
        buzzerSet(&buzzer, 1);
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
  buzzerRun(&led);
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
void analogRun(void)
{
  if (accu.count > accu.readTime) {
    accu.rawData = analogMean(analogRead(accu.Pin));
    accu.count = 0;
  } else {
    accu.count += LOOPDELAY;
  }
}

int analogMean(int data){
  accu.sum-=accu.data[accu.index];
  accu.sum+=data;
  accu.data[accu.index]=data;
  accu.index++;
  if (accu.index>(sizeof(accu.data)/sizeof(int)-1)){
    accu.index=0;
  }
  return(accu.sum/(sizeof(accu.data)/sizeof(int)));  
}

void buzzerRun(buzzerStr *data) {
  if (data->Cmd != 0) {
    if (data->State == true and data->Count <= data->Time) {
      digitalWrite(data->Pin, HIGH);
      data->Count += LOOPDELAY;
      if (data->Count >= data->Time) {
        data->State = false;
        data->Count = 0;
      }
    }
    if (data->State == false and data->Count <= data->Time) {
      digitalWrite(data->Pin, LOW);
      data->Count += LOOPDELAY;
      if (data->Count >= data->Time) {
        data->State = false;
        data->Count = 0;
        if (data->Cmd != 0) {
          if (data->Cmd > 0) {
            data->Cmd -= 1;
          }
          data->State = true;
        }
      }
    }
  }
}

void buzzerSet(buzzerStr *data, byte nb)
{
  if (data->Cmd>0){
    data->Cmd+=nb;
  }else{
    data->Cmd=nb;
    data->State=true;
  }
}


void baseA_Interrupt(void) {
  if ((baseA.old_event + baseA.rebundBtn_time) < millis()) {
    baseCheck(baseA.Pin);
    baseA.old_event=millis();
    baseA.nbInterrupt++;
  }
}

void baseB_Interrupt(void) {
  if ((baseB.old_event + baseB.rebundBtn_time) < millis()) {
    baseCheck(baseB.Pin);
    baseB.old_event=millis();
    baseB.nbInterrupt++;
  }
}

void baseCheck(byte base) {
  if (chrono_mode==Training){
    Serial.println("baseCheckTraining");
    baseCheckTraining(base);    
  }else if (chrono_mode==Race){
    Serial.println("baseCheckRace");
    baseCheckRace(base);
  }
}

void baseCheckTraining(byte base){
  if (chronostatus.runStatus==InStart and (base == BASEAPIN or base == BTNNEXTPIN)){
    chrono.oldtime=millis();
    chronostatus.runStatus=InProgressB;
  }else if (chronostatus.runStatus==InStart and (base == BASEBPIN or base == BTNNEXTPIN)) {
    chrono.oldtime=millis();
    chronostatus.runStatus=InProgressA;
  }else if (chronostatus.runStatus==InProgressA and (base == BASEAPIN or base == BTNNEXTPIN)){
    chronostatus.runStatus=InProgressB;
    trainingSetTime ();
  }else if (chronostatus.runStatus==InProgressB and (base == BASEBPIN or base == BTNNEXTPIN)) {
    chronostatus.runStatus=InProgressA;
    trainingSetTime ();
  }
  buzzer.Cmd = 1;
}

void trainingSetTime(void){
  unsigned long time1=0;
  time1 = millis();
  if (chrono.lapCount>10){
    memcpy(chrono.lap, &chrono.lap[1], sizeof (unsigned long)*9);
    chrono.lap[9] = time1 - chrono.oldtime;
    chrono.lapCount++;    
  }else{
    chrono.lap[chrono.lapCount] = time1 - chrono.oldtime;
    chrono.lapCount++;
  }
  chrono.oldtime = time1;
}

void baseCheckRace(byte base){
  unsigned long time1=0;
  if (chronostatus.runStatus==Launched and (BASEAPIN == base or base == BTNNEXTPIN)) {
    chronostatus.runStatus = InStart;
    buzzerSet(&buzzer, 1);
  }else if (chronostatus.runStatus==Late and (BASEAPIN == base or base == BTNNEXTPIN)){
    chronostatus.runStatus = InStart_Late;
    buzzerSet(&buzzer, 1);
  }else if (chronostatus.runStatus==InStart and (BASEAPIN == base or base == BTNNEXTPIN)) {
    buzzerSet(&buzzer, 1);
    chronostart();
    chronostatus.runStatus = InProgressB;
  }else if (chronostatus.runStatus==InStart_Late and (BASEAPIN == base or base == BTNNEXTPIN)){
    chronostatus.runStatus = InProgressB;
    buzzerSet(&buzzer, 1);
  }else if (chronostatus.runStatus==InProgressA and (base == BASEAPIN or base == BTNNEXTPIN)) {
    time1 = millis();
    chrono.lap[chrono.lapCount] = time1 - chrono.oldtime;
    chrono.lapCount++;
  
    chrono.oldtime = time1;
    buzzer.Cmd = 1;
    if (chrono.lapCount >= 10) {
      chronostatus.runStatus = WaitAltitude;
      chrono.startaltitudetime = millis();
      buzzerSet(&buzzer, 3);
    } else {
      chronostatus.runStatus = InProgressB;
    }
  }else if (chronostatus.runStatus==InProgressB and (base == BASEBPIN or base == BTNNEXTPIN)) {
    time1 = millis();
    chrono.lap[chrono.lapCount] = time1 - chrono.oldtime;
    /*Serial.print("chronoInProgressB,lapCount ");
    Serial.print(chrono.lapCount);
    Serial.print(",oldtime ");
    Serial.print(chrono.oldtime);
    Serial.print(",time1 ");
    Serial.print(time1);
    Serial.println(",");
    */chrono.oldtime = time1;
    chrono.lapCount++;
    chronostatus.runStatus = InProgressA;
    if (chrono.lapCount == 9) {
      buzzerSet(&buzzer, 2);
    }else{
      buzzerSet(&buzzer, 1);
    }
  }else if (chronostatus.runStatus==WaitAltitude and (chrono.startaltitudetime + 5000) < millis()) {
    buzzer.Cmd = 3;
    chronostatus.runStatus = Finished;
  }else if ((chronostatus.runStatus==InWait or chronostatus.runStatus==Finished) and (base == BASEAPIN or base == BASEBPIN)){
      buzzerSet(&buzzer, 1);
  }
}

void chronostart(void){
  if (chrono.started==false){
    chrono.starttime=millis();
    chrono.started=true;
    chrono.oldtime=chrono.starttime;
    Serial.println("chrono started,");
  }
  chrono.lapCount=0;
}

void printbuzzer(void){
  Serial.print("buzzertime,");
  Serial.print(buzzer.Time);
  Serial.println(",");
}

void printbase(void){
  Serial.print("baseA,");
  Serial.print("rebundtime,");
  Serial.print(baseA.rebundBtn_time);
  Serial.print(",nbinterrrupt,");
  Serial.print(baseA.nbInterrupt);
  Serial.print(",baseB");
  Serial.print(",rebundtime,");
  Serial.print(baseA.rebundBtn_time);
  Serial.print(",nbinterrrupt,");
  Serial.print(baseB.nbInterrupt);
  Serial.println(",");
}

void printstatus(void){
  Serial.print("status,");
  Serial.print(chronostatus.runStatus);
  Serial.println(",");
}

void printmode(void){
  Serial.print("mode,");
  Serial.print(chrono_mode);
  Serial.println(",");
}

void printchrono(void){
  Serial.print("lap,");
  Serial.print(chrono.lapCount);
  for (i = 0; i < (chrono.lapCount<=10?chrono.lapCount:10); i++) {
    Serial.print(",");
    Serial.print(chrono.lap[i]);
  }
  Serial.println(",");
}

void printreset(void){
  Serial.println("resetµc,F3F,Chrono,available,");
}

void printvoltage(void){
  Serial.print("voltage,");
  Serial.print(accu.rawData);
  Serial.println(",");
}

void printresetchrono(void){
  Serial.print("reset");
  Serial.println(",");
}

void printforcebaseA(void){
  Serial.print("force baseA");
  Serial.println(",");
}

void printforcebaseB(void){
  Serial.print("force baseB");
  Serial.println(",");
}

void printforcebtnnext(void){
  Serial.print("force btn next");
  Serial.println(",");
}

void printdebug(void){
  printmode();
  printstatus();
  printchrono();
  printbase();
  printvoltage();
  led.Cmd = -1;
  Serial.print("buzzer,");
  Serial.print("cmd,");
  Serial.print(buzzer.Cmd);
  Serial.print(",time,");
  Serial.print(buzzer.Time);
  Serial.print(",state,");
  Serial.print(buzzer.State);
  Serial.print(",led,");
  Serial.print("cmd,");
  Serial.print(led.Cmd);
  Serial.print(",time,");
  Serial.print(led.Time);
  Serial.print(",state,");
  Serial.print(led.State);
  Serial.println(",");
}
