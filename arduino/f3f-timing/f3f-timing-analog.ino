const byte VOLTAGEPIN0 = A0;
const byte VOLTAGEPIN1 = A1;
const int VOLTAGE_TIME = 2000;
const int INITIAL_RAW_VOLTAGE = 900;

typedef struct {
  int readTime;
  int count;
  byte Pin;
  int data[10];
  byte index;
  int sum;
  int rawData;
} analogStr;

volatile analogStr accu[2] = {0, 0};

void analog_setup(void){
  memset (accu, 0, sizeof(accu)*2);
  accu[0].Pin = VOLTAGEPIN0;
  accu[0].readTime = VOLTAGE_TIME;
  //Initalize @12V for the first measurements
  accu[0].rawData = INITIAL_RAW_VOLTAGE;
  accu[0].sum = INITIAL_RAW_VOLTAGE*sizeof(accu[0].data)/sizeof(int);
  int i;
  for (i=0; i<sizeof(accu[0].data)/sizeof(int);i++){
    accu[0].data[i]=INITIAL_RAW_VOLTAGE;
  }

  accu[1].Pin = VOLTAGEPIN1;
  accu[1].readTime = VOLTAGE_TIME;
  //Initalize @12V for the first measurements
  accu[1].rawData = INITIAL_RAW_VOLTAGE;
  accu[1].sum = INITIAL_RAW_VOLTAGE*sizeof(accu[1].data)/sizeof(int);
  for (i=0; i<sizeof(accu[1].data)/sizeof(int);i++){
    accu[1].data[i]=INITIAL_RAW_VOLTAGE;
  }
}

void analogRun(void)
{
  int i;
  for (i=0; i<2; i++){
    if (accu[i].count > accu[i].readTime) {
      accu[i].rawData = analogMean(i, analogRead(accu[i].Pin));
      accu[i].count = 0;
    } else {
      accu[i].count += LOOPDELAY;
    }    
  }
}

int analogMean(int num, int data){
  accu[num].sum-=accu[num].data[accu[num].index];
  accu[num].sum+=data;
  accu[num].data[accu[num].index]=data;
  accu[num].index++;
  if (accu[num].index>(sizeof(accu[num].data)/sizeof(int)-1)){
    accu[num].index=0;
  }
  return(accu[num].sum/(sizeof(accu[num].data)/sizeof(int)));  
}

void printvoltage(void){
  Serial.print("voltage,");
  Serial.print(accu[0].rawData);
  Serial.print(",");
  Serial.print(accu[1].rawData);
  Serial.println(",");
}
