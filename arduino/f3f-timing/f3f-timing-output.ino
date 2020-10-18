

volatile buzzerStr buzzer = {0};
volatile buzzerStr led = {0};

void output_setup(void){
  memset (&buzzer, 0, sizeof(buzzer));
  memset (&led, 0, sizeof(led));
  buzzer.Time = BUZZERTIME;
  buzzer.Pin = BUZZERPIN;

  led.Time = LEDTIME;
  led.Pin = LED_BUILTIN;
  // initialize digital pin LED_BUILTIN and buzzer PIN as an output.
  pinMode(buzzer.Pin, OUTPUT);
  pinMode(led.Pin, OUTPUT);
}

void buzzerRun(void) {
  if (buzzer.Cmd != 0) {
    if (buzzer.State == true and buzzer.Count <= buzzer.Time) {
      digitalWrite(buzzer.Pin, HIGH);
      buzzer.Count += LOOPDELAY;
      if (buzzer.Count >= buzzer.Time) {
        buzzer.State = false;
        buzzer.Count = 0;
      }
    }
    if (buzzer.State == false and buzzer.Count <= buzzer.Time) {
      digitalWrite(buzzer.Pin, LOW);
      buzzer.Count += LOOPDELAY;
      if (buzzer.Count >= buzzer.Time) {
        buzzer.State = false;
        buzzer.Count = 0;
        if (buzzer.Cmd != 0) {
          if (buzzer.Cmd > 0) {
            buzzer.Cmd -= 1;
          }
          buzzer.State = true;
        }
      }
    }
  }
}

void buzzerSet(byte nb)
{
  if (buzzer.Cmd==0){
    buzzer.Cmd=nb;
    buzzer.State=true;
  }
}

void printbuzzer(void){
  Serial.print("buzzertime,");
  Serial.print(buzzer.Time);
  Serial.println(",");
}

void printoutput(void){
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
