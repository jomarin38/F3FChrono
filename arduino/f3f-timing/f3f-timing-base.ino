const byte BASEAPIN = 2;
const byte BASEBPIN = 3;
const byte BTNNEXTPIN = -1; //Not a real btn

const int REBUNDTIME = 500;

typedef struct {
  unsigned long old_event;
  unsigned long rebundBtn_time;
  unsigned long nbInterrupt;
  byte Pin;
} baseEventStr;

volatile baseEventStr baseA = {0}, baseB = {0};

void base_setup(void){
  memset (&baseA, 0, sizeof(baseA));
  baseA.rebundBtn_time = REBUNDTIME;
  baseA.Pin = BASEAPIN;

  memset (&baseB, 0, sizeof(baseB));
  baseB.rebundBtn_time = REBUNDTIME;
  baseB.Pin = BASEBPIN;
  //Initialize buttons pin in interrupt mode
  pinMode(baseA.Pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(baseA.Pin), baseA_Interrupt, FALLING);
  pinMode(baseB.Pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(baseB.Pin), baseB_Interrupt, FALLING);
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
