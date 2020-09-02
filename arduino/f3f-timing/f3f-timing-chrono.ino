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
  Race = 0,
  Training
};

typedef struct {
  byte lapCount;
  byte started;
  unsigned long lap[10];
  unsigned long oldtime;
  unsigned long starttime;
  unsigned long startaltitudetime;
  unsigned long climbout_time, oldclimbout_time;
}chronoStr;

typedef struct {
  int runStatus;
}chronoStatusStr;

volatile chronoStr chrono = {0}, chrono_old = {0};
volatile chronoStatusStr chronostatus, chronostatus_old;
volatile chronoMode chrono_mode = Race;

extern void buzzerSet(byte nb);

void chrono_setup(void){
  memset (&chrono, 0, sizeof(chrono));
  memset (&chrono_old, 0, sizeof(chrono_old));
  memset (&chronostatus, 0, sizeof(chronostatus));
  memset (&chronostatus_old, 0, sizeof(chronostatus_old));
  chrono_mode = Race;
  chronostatus.runStatus = InWait;
}

void chrono_run(void){
  if (chronostatus.runStatus == WaitAltitude) {
    baseCheck(0);
  } 
}

void baseCheck(byte base) {
  if (chrono_mode==Training){
    baseCheckTraining(base);    
  }else if (chrono_mode==Race){
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
  buzzerSet(1);
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
    buzzerSet(1);
  }else if (chronostatus.runStatus==Late and (BASEAPIN == base or base == BTNNEXTPIN)){
    chronostatus.runStatus = InStart_Late;
    buzzerSet(1);
  }else if (chronostatus.runStatus==InStart and (BASEAPIN == base or base == BTNNEXTPIN)) {
    buzzerSet(1);
    time1=millis();
    chrono.climbout_time = time1 - chrono.oldtime;
    chrono.oldtime=time1;
    chronostatus.runStatus = InProgressB;
  }else if (chronostatus.runStatus==InStart_Late and (BASEAPIN == base or base == BTNNEXTPIN)){
    chronostatus.runStatus = InProgressB;
    time1=millis();
    chrono.climbout_time = time1 - chrono.oldtime;
    chrono.oldtime=time1;
    buzzerSet(1);
  }else if (chronostatus.runStatus==InProgressA and (base == BASEAPIN or base == BTNNEXTPIN)) {
    time1 = millis();
    chrono.lap[chrono.lapCount] = time1 - chrono.oldtime;
    chrono.lapCount++;
  
    chrono.oldtime = time1;
    buzzerSet(1);
    if (chrono.lapCount >= 10) {
      chronostatus.runStatus = WaitAltitude;
      chrono.startaltitudetime = millis();
      buzzerSet(2);
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
      buzzerSet(2);
    }else{
      buzzerSet(1);
    }
  }else if (chronostatus.runStatus==WaitAltitude and (chrono.startaltitudetime + 5000) < millis()) {
    buzzerSet(3);
    chronostatus.runStatus = Finished;
  }else if ((chronostatus.runStatus==InWait or chronostatus.runStatus==Finished) and (base == BASEAPIN or base == BASEBPIN)){
      buzzerSet(1);
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

void printclimbout_time(void){
  Serial.print("climbout_time,");
  Serial.print(chrono.climbout_time);
  Serial.println(",");
}

void printresetchrono(void){
  Serial.print("reset");
  Serial.println(",");
}
