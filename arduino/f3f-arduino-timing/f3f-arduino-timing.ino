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
  byte runStatus;
  byte lapCount;
  unsigned long lap[10];
  unsigned long time1;
  unsigned long oldtime;
  unsigned long starttime;
  unsigned long startaltitudetime;
} chronoStr;

enum i2c_request {
  setStatus = 1,
  setBuzzerTime,
  setRebundBtn,
  eventBaseA,
  resetChrono,
  reboot,
  getData,
  getData1
};

typedef struct {
  byte data[10];
  byte nbData;
} i2cReceiveStr;

typedef struct {
  byte data[30];
  byte nbData;
} i2cSendStr;

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
volatile i2cReceiveStr i2cReceive = {0};
volatile i2cSendStr i2cSend = {0};
volatile serialStr serial;
volatile baseEventStr baseA = {0}, baseB = {0};
volatile analogStr accu = {0};
volatile buzzerStr buzzer = {0};
volatile buzzerStr led = {0};
volatile debugStr debug = {0};
volatile unsigned int i = 0;
volatile byte temp = 0;

void(* resetFunc) (void) = 0;//declare reset function at address 0
void baseA_Interrupt(void);
void baseB_Interrupt(void);
void sendData(void);
void receiveData(int byteCount);
void baseCheck(byte base);
void debugRun(void);
void analogRun(void);
void buzzerRun(buzzerStr *data);
void buzzerSet(buzzerStr *data, byte nb);
void baseCheck(byte base);

// the setup function runs once when you press reset or power the board
void setup() {
  //Initialize chrono var.
  memset (&debug, 0, sizeof(debug));
  memset (&chrono, 0, sizeof(chrono));
  memset (&chrono_old, 0, sizeof(chrono_old));

  //Initialize I2C link as slave with Rpi
  memset (&i2cReceive, 0, sizeof(i2cReceive));
  memset (&i2cSend, 0, sizeof(i2cSend));
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

  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  //Only for debug
  Serial.begin(57600);
  while (!Serial) {
    delay(100);
    Serial.println("F3F timer connected");
  }
}

// the loop function runs over and over again forever
void loop() {
  debugRun();
  analogRun();
  buzzerRun(&buzzer);
  if (chrono.runStatus == WaitAltitude) {
    baseCheck(0);
  }
  delay (LOOPDELAY);
}


void debugRun(void) {
  temp = memcmp (&chrono, &chrono_old, sizeof(chrono));
  if (temp != 0){
    Serial.print("s");
    Serial.print(chrono.runStatus);
    Serial.print(",");
    Serial.print(chrono.lapCount);
    for (i = 0; i < chrono.lapCount; i++) {
      Serial.print(",");
      Serial.print(chrono.lap[i]);
    }
    Serial.println("");
    memcpy(&chrono_old, &chrono, sizeof(chrono));
  }
  if (serial.data_available) {
    char tmp = serial.data_read[0];
    Serial.println(tmp);
    if (tmp=='t'){
      buzzer.Time=0;
      for (i=1; i<serial.nb_data-1; i++){
        buzzer.Time = buzzer.Time*10+(int)(serial.data_read[i]-'0');
      }
      led.Time = buzzer.Time;
      Serial.println(buzzer.Time);
    }else if (tmp=='l'){
      Serial.print("Lap count : ");
      Serial.println(chrono.lapCount);
      for (i = 0; i < chrono.lapCount; i++) {
        Serial.print("Lap : ");
        Serial.println(i);
        Serial.println((float)chrono.lap[i] / 1000);
      }
    }else if (tmp=='d'){
      led.Cmd = -1;
      Serial.println("buzzer :");
      Serial.print("cmd ");
      Serial.println(buzzer.Cmd);
      Serial.print("time ");
      Serial.println(buzzer.Time);
      Serial.print("state ");
      Serial.println(buzzer.State);
      Serial.println("led : ");
      Serial.print("cmd ");
      Serial.println(led.Cmd);
      Serial.print("time ");
      Serial.println(led.Time);
      Serial.print("state ");
      Serial.println(led.State);
    }else if (tmp=='s'){
      chrono.runStatus=byte(serial.data_read[1]-'0');
      String data ="status : ";
      data+= chrono.runStatus;
      Serial.println(data);
    }else if (tmp=='b'){
      Serial.println("base A :");
      Serial.print("rebund time : ");
      Serial.println(baseA.rebundBtn_time);
      Serial.print("nb interrrupt : ");
      Serial.println(baseA.nbInterrupt);
      Serial.println("base B :");
      Serial.print("rebund time : ");
      Serial.println(baseA.rebundBtn_time);
      Serial.print("nb interrrupt : ");
      Serial.println(baseB.nbInterrupt);
    }else if (tmp=='v'){
      Serial.print("voltage : ");
      Serial.println(accu.rawData);
    }else if (tmp=='r'){
      baseA.rebundBtn_time=0;
      for (i=1; i<serial.nb_data-1; i++){
        baseA.rebundBtn_time = baseA.rebundBtn_time*10+(int)(serial.data_read[i]-'0');
      }
      baseB.rebundBtn_time = baseA.rebundBtn_time;
    }
    
  memset(&serial, 0, sizeof(serial));
  buzzerRun(&led);
  }
}

void serialEvent(){
  while (Serial.available()){
    if (serial.data_available==false){
      serial.data_read[serial.nb_data]=(char)Serial.read();
      if (serial.data_read[serial.nb_data]=='.'){
        Serial.print("data available : ");
        Serial.println((char*)serial.data_read);
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

// callback for received data
void receiveData(int byteCount) {
  memset(&i2cReceive, 0, sizeof(i2cReceive));
  while (Wire.available() and i2cReceive.nbData < sizeof (i2cReceive.data)) {
    i2cReceive.data[i2cReceive.nbData] = Wire.read();
    i2cReceive.nbData++;
  }

  switch (i2cReceive.data[0]) {
    case setStatus:
      chrono.runStatus = i2cReceive.data[1];
      break;
    case eventBaseA:
      baseCheck(BASEAPIN);
      break;
    case setBuzzerTime:
      buzzer.Time = (i2cReceive.data[1] & 0xff) | ((i2cReceive.data[2] << 8) & 0xff00);
      break;
    case setRebundBtn:
      baseA.rebundBtn_time = (i2cReceive.data[1] & 0xff) | ((i2cReceive.data[2] << 8) & 0xff00);
      baseB.rebundBtn_time = (i2cReceive.data[1] & 0xff) | ((i2cReceive.data[2] << 8) & 0xff00);
      break;
    case resetChrono:
      memset(&chrono, 0, sizeof(chronoStr));
      break;
    case reboot:
      resetFunc();
      break;
    default:
      break;
  }
}

// callback for sending data
void sendData() {
  memset(&i2cSend, 0, sizeof(i2cSend));
  switch (i2cReceive.data[0]) {
    case getData:
      i2cSend.data[0] = chrono.runStatus;
      memcpy(&i2cSend.data[1], &accu.rawData, 2);
      i2cSend.data[3] = chrono.lapCount;
      memcpy(&i2cSend.data[4], chrono.lap, 12);
      i2cSend.nbData = 32;
      break;
    case getData1:
      memcpy(i2cSend.data, &chrono.lap[3], 32);
      i2cSend.nbData = 32;
      break;
    default:
      break;
  }
  Wire.write((byte *)i2cSend.data, i2cSend.nbData);
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
  switch (chrono.runStatus) {
    case Launched :
      if (BASEAPIN == base) {
        chrono.runStatus = InStart;
        buzzerSet(&buzzer, 1);
      }
      break;
    case InStart:
      if (BASEAPIN == base) {
        buzzerSet(&buzzer, 1);
        chrono.time1 = millis();
        chrono.oldtime = chrono.time1;
        chrono.lapCount=0;
        chrono.runStatus = InProgressB;
      }
      break;
    case InProgressA:
      if (base == BASEAPIN) {
        chrono.time1 = millis();
        chrono.lap[chrono.lapCount] = chrono.time1 - chrono.oldtime;
        chrono.lapCount++;

        chrono.oldtime = chrono.time1;
        buzzer.Cmd = 1;
        if (chrono.lapCount >= 10) {
          chrono.runStatus = WaitAltitude;
          chrono.startaltitudetime = millis();
          buzzerSet(&buzzer, 3);
        } else {
          chrono.runStatus = InProgressB;
        }
      }
      break;
    case InProgressB:
      if (base == BASEBPIN) {
        chrono.time1 = millis();
        chrono.lap[chrono.lapCount] = chrono.time1 - chrono.oldtime;
        chrono.oldtime = chrono.time1;
        chrono.lapCount++;
        chrono.runStatus = InProgressA;
        if (chrono.lapCount == 9) {
          buzzerSet(&buzzer, 2);
        }else{
          buzzerSet(&buzzer, 1);
        }
      }else{
        if (base == BASEAPIN and chrono.lapCount==0){
          buzzerSet(&buzzer, 1);
        }
      }
      break;
    case WaitAltitude:
      if ((chrono.startaltitudetime + 5000) < millis()) {
        buzzer.Cmd = 3;
        chrono.runStatus = Finished;
      }
      break;
    default:
        buzzerSet(&buzzer, 1);
      break;
  }
}
