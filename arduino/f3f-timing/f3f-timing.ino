/*
  F3F Timing
  use 2 pins as interrupt mode
*/
#include <Wire.h>

const float VERSION = 0.92;
const byte LOOPDELAY = 5;

const byte BUZZERPIN = 12;
const int BUZZERTIME = 300;
const int LEDTIME = 300;

typedef struct {
  byte state;
  byte received;
} debugStr;


typedef struct {
  int Time;     //in milliseconds
  int Count;    //in milliseconds
  int Cmd;      //blink number
  byte State;   //buzzer state
  byte Pin;
}buzzerStr;

volatile debugStr debug = {0};
volatile unsigned int i = 0;
volatile byte temp = 0;
volatile byte reset = true;


void(* resetFunc) (void) = 0;

void buzzerRun(buzzerStr *data);
void buzzerSet(buzzerStr *data, byte nb);
void chrono_setup(void);
void baseCheck(byte base);
void serial_setup(void);
void serial_run(void);



// the setup function runs once when you press reset or power the board
void setup() {
  //Initialize chrono var.
  memset (&debug, 0, sizeof(debug));
  serial_setup();
  chrono_setup();
  output_setup();
  analog_setup();
  base_setup();
}

// the loop function runs over and over again forever
void loop() {
  baseA_check();
  baseB_check();
  serial_run();
  analogRun();
  buzzerRun();
  chrono_run();
  delay (LOOPDELAY);
  
}

void printreset(void){
  Serial.println("resetµc,F3F,Chrono,available,");
}
