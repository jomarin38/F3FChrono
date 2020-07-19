const byte VOLTAGEPIN = A1;
const int VOLTAGE_TIME = 2000;

typedef struct {
  int readTime;
  int count;
  byte Pin;
  int data[10];
  byte index;
  int sum;
  int rawData;
} analogStr;

volatile analogStr accu = {0};

void analog_setup(void){
  memset (&accu, 0, sizeof(accu));
  accu.Pin = VOLTAGEPIN;
  accu.readTime = VOLTAGE_TIME;
  accu.rawData= 900; //Initalize @12V for the first measurements
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

void printvoltage(void){
  Serial.print("voltage,");
  Serial.print(accu.rawData);
  Serial.println(",");
}
