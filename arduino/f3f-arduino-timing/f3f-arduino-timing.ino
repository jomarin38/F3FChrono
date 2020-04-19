/*
  F3F Timing
  use 2 pins as interrupt mode
*/
#include <Wire.h>

#define SLAVE_ADDRESS 0x05
const byte BASEAPIN = 2;
const byte BASEBPIN = 3;
const byte VOLTAGEPIN = A1;
const byte BUZZERPIN = 12;
const byte LOOPDELAY = 100;
const int BUZZERTIME = 300;
const int LEDTIME = 300;

enum chronoStatus {
  InWait = 0,
  WaitLaunch,
  Launched,
  InStart,
  InProgressA,
  InProgressB,
  WaitAltitude,
  Finished
};

typedef struct {
  byte lapCount;
  unsigned long lap[10];
  unsigned long time1;
  unsigned long oldtime;
  unsigned long starttime;
  unsigned long startaltitudetime;
} chronoStr;

typedef struct {
  int runStatus;
}chronoStatusStr;


typedef struct{
  char data_read[100];
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
  int rawData;
  byte Pin;
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

/*void baseA_Interrupt(void);
void baseB_Interrupt(void);
void baseCheck(byte base);
void RS232Run(void);
void analogRun(void);
void buzzerRun(buzzerStr *data);
void buzzerSet(buzzerStr *data, byte nb);
void baseCheck(byte base);
*/
// the setup function runs once when you press reset or power the board
void setup() {
  //Initialize chrono var.
  memset (&debug, 0, sizeof(debug));
  memset (&chrono, 0, sizeof(chrono));
  memset (&chrono_old, 0, sizeof(chrono_old));
  memset (&chronostatus, 0, sizeof(chronostatus));
  memset (&chronostatus_old, 0, sizeof(chronostatus_old));

  memset (&buzzer, 0, sizeof(buzzer));
  memset (&led, 0, sizeof(led));
  memset (&accu, 0, sizeof(accu));
  memset (&serial,0, sizeof(serial));

  buzzer.Time = BUZZERTIME;
  buzzer.Pin = BUZZERPIN;

  led.Time = LEDTIME;
  led.Pin = LED_BUILTIN;

  accu.Pin = VOLTAGEPIN;
  accu.readTime = 2000;
  accu.rawData= 900; //Initalize @12V for the first measurements
  
  memset (&baseA, 0, sizeof(baseA));
  baseA.rebundBtn_time = 200;
  baseA.Pin = BASEAPIN;

  memset (&baseB, 0, sizeof(baseB));
  baseB.rebundBtn_time = 200;
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
    Serial.println("F3F timer connected");
  }
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
  //check if status changed
  temp = memcmp (&chronostatus, &chronostatus_old, sizeof(chronostatus));
  if (temp != 0){
    Serial.print("status,");
    Serial.print(chronostatus.runStatus);
    Serial.println(",");
    memcpy(&chronostatus_old, &chronostatus, sizeof(chronostatus));
  }
  //check if lap changed
  temp = memcmp (&chrono, &chrono_old, sizeof(chrono));
  if (temp != 0){
    Serial.print("lap,");
    Serial.print(chrono.lapCount);
    for (i = 0; i < chrono.lapCount; i++) {
      Serial.print(",");
      Serial.print(chrono.lap[i]);
    }
    Serial.println(",");
    memcpy(&chrono_old, &chrono, sizeof(chrono));
  }
  //Process serial request
  if (serial.data_available) {
    char tmp = serial.data_read[0];
    if (tmp=='t'){
      buzzer.Time=0;
      for (i=1; i<serial.nb_data-1; i++){
        buzzer.Time = buzzer.Time*10+(int)(serial.data_read[i]-'0');
      }
      led.Time = buzzer.Time;
      Serial.print(buzzer.Time);
      Serial.println(",");
    }else if (tmp=='d'){
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
    }else if (tmp=='s'){
      chronostatus.runStatus=byte(serial.data_read[1]-'0');
    }else if (tmp=='b'){
      baseA.rebundBtn_time=0;
      for (i=1; i<serial.nb_data-1; i++){
        baseA.rebundBtn_time = baseA.rebundBtn_time*10+(int)(serial.data_read[i]-'0');
      }
      baseB.rebundBtn_time = baseA.rebundBtn_time;
      Serial.print("base A,");
      Serial.print("rebund time,");
      Serial.print(baseA.rebundBtn_time);
      Serial.print(",nb interrrupt,");
      Serial.print(baseA.nbInterrupt);
      Serial.print(",base B");
      Serial.print(",rebund time,");
      Serial.print(baseA.rebundBtn_time);
      Serial.print(",nb interrrupt,");
      Serial.print(baseB.nbInterrupt);
      Serial.println(",");
    }else if (tmp=='v'){
      Serial.print("voltage,");
      Serial.print(accu.rawData);
      Serial.println(",");
    }else if (tmp=='r'){
      memset(&chronostatus, 0, sizeof(chronostatus));
      memset(&chrono, 0, sizeof(chrono));
      Serial.print("reset");
      Serial.println(",");
    }else if (tmp=='e'){
      baseCheck(baseA.Pin);
      Serial.print("force baseA");
      Serial.println(",");
    }
    
    memset(&serial, 0, sizeof(serial));
  }
  buzzerRun(&led);
}

void serialEvent(){
  while (Serial.available()){
    if (serial.data_available==false){
      serial.data_read[serial.nb_data]=(char)Serial.read();
      if (serial.data_read[serial.nb_data]=='.'){
        serial.data_available=true;
      }
      serial.nb_data++;
    }    
  }  
}
void analogRun(void)
{
  if (accu.count > accu.readTime) {
    accu.rawData = analogRead(accu.Pin);
    accu.count = 0;
  } else {
    accu.count += LOOPDELAY;
  }
}

void buzzerRun(buzzerStr *data) {
  if (data->Cmd != 0) {
    if (data->State == true & data->Count <= data->Time) {
      digitalWrite(data->Pin, HIGH);
      data->Count += LOOPDELAY;
      if (data->Count >= data->Time) {
        data->State = false;
        data->Count = 0;
      }
    }
    if (data->State == false & data->Count <= data->Time) {
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
  if (chronostatus.runStatus==Launched and BASEAPIN == base) {
    chronostatus.runStatus = InStart;
    buzzerSet(&buzzer, 1);
  }else if (chronostatus.runStatus==InStart and BASEAPIN == base) {
    buzzerSet(&buzzer, 1);
    chrono.time1 = millis();
    chrono.oldtime = chrono.time1;
    chrono.lapCount=0;
    chronostatus.runStatus = InProgressB;
  }else if (chronostatus.runStatus==InProgressA and base == BASEAPIN) {
    chrono.time1 = millis();
    chrono.lap[chrono.lapCount] = chrono.time1 - chrono.oldtime;
    chrono.lapCount++;
  
    chrono.oldtime = chrono.time1;
    buzzer.Cmd = 1;
    if (chrono.lapCount >= 10) {
      chronostatus.runStatus = WaitAltitude;
      chrono.startaltitudetime = millis();
      buzzerSet(&buzzer, 3);
    } else {
      chronostatus.runStatus = InProgressB;
    }
  }else if (chronostatus.runStatus==InProgressB and base == BASEBPIN) {
    chrono.time1 = millis();
    chrono.lap[chrono.lapCount] = chrono.time1 - chrono.oldtime;
    chrono.oldtime = chrono.time1;
    chrono.lapCount++;
    chronostatus.runStatus = InProgressA;
    if (chrono.lapCount == 9) {
      buzzerSet(&buzzer, 2);
    }else{
      buzzerSet(&buzzer, 1);
    }
  }else if (chronostatus.runStatus==InProgressB and base == BASEAPIN and chrono.lapCount==0){
    buzzerSet(&buzzer, 1);
  }else if (chronostatus.runStatus==WaitAltitude and (chrono.startaltitudetime + 5000) < millis()) {
    buzzer.Cmd = 3;
    chronostatus.runStatus = Finished;
  }else{
    if (base == BASEAPIN or base == BASEBPIN){
      buzzerSet(&buzzer, 1);
    }
  }
}
