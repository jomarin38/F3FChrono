/*
  Software serial multple serial test

 Receives from the hardware serial, sends to software serial.
 Receives from software serial, sends to hardware serial.

 The circuit:
 * RX is digital pin 10 (connect to TX of other device)
 * TX is digital pin 11 (connect to RX of other device)

 Note:
 Not all pins on the Mega and Mega 2560 support change interrupts,
 so only the following can be used for RX:
 10, 11, 12, 13, 50, 51, 52, 53, 62, 63, 64, 65, 66, 67, 68, 69

 Not all pins on the Leonardo and Micro support change interrupts,
 so only the following can be used for RX:
 8, 9, 10, 11, 14 (MISO), 15 (SCK), 16 (MOSI).

 created back in the mists of time
 modified 25 May 2012
 by Tom Igoe
 based on Mikal Hart's example

 This example code is in the public domain.

 */

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;

float wind_dir = 0.0;
float wind_speed = 0.0;


/*
 * For the display
 */
#define SIZ_BUF_RX 100

#define TRUE     1
#define FALSE     0
#define ON      1
#define OFF     0
#define OK      1
#define NO      0
#define YES     1
#define ERR     0
#define CR      13
#define EOS     0         //end of string


#define LNG_LINE 16

#define BACKLIGHT 0


char screen_buffer[SIZ_BUF_RX];
char speed_str[5];
char dir_str[6];

float current_speed = 0.0;
float current_dir = 0.0;
long  last_reception_time = 0;

int timeout_delay = 10000;


void setup() {

  SPI_MasterInit();
  

  delay(300);
  SPI_MasterTransfer(0xFE);
  SPI_MasterTransfer(0x53);           //Set backlight brightness
  SPI_MasterTransfer(4);              //because at fireing brightness if full
  
  //__start screen
  sprintf(screen_buffer, "Waiting for data ...");
  Display_2x16(ON, screen_buffer);
  delay(1500);

  // set the data rate for the SoftwareSerial port
  //mySerial.begin(9600);
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
}

void loop() { // run over and over
  recvWithEndMarker();
  parseData();
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
            last_reception_time = millis();
        }
    }
}

void showData() {
    //Serial.print("Speed : ");Serial.print(wind_speed);Serial.print("\t");
    //Serial.print("Direction : ");Serial.print(wind_dir);Serial.println();

    dtostrf(wind_speed, 4, 1, speed_str);
    dtostrf(wind_dir, 5, 1, dir_str);
    sprintf(screen_buffer, "Speed : %s m/sDir  : %s deg", speed_str, dir_str);
    Display_2x16(ON, screen_buffer);
    //delay(1000);
}

void parseData() {
    String buff = receivedChars;
    buff.trim();
    if (newData == true && buff.length()>0) {
        //Serial.print(receivedChars); Serial.print(" # ");
        if (receivedChars[5]=='s') {
          wind_speed = getReceivedValue();
        }
        else if (receivedChars[5]=='d') {
          wind_dir = getReceivedValue();
        }
        showData();
        newData=false;
    }
    else {
      newData=false;
      if ((millis() - last_reception_time)>timeout_delay) {
        sprintf(screen_buffer, "Waiting for data ...");
        Display_2x16(ON, screen_buffer);
        delay(1500);
      }
    }
}

float getReceivedValue() {
    String s = "";
    bool parsing_completed = false;
    bool searching = true;
    bool waiting_for_data = true;
    int i = 0;
    while(!parsing_completed) {
      char current_char = receivedChars[i];
      if (searching) {
        if (current_char==' ') {
          searching=false;
          waiting_for_data=true;
        }
      }
      else {
        if (current_char!=' ') {
          s+=current_char;
          waiting_for_data = false;
        }
        else {
          if (!(waiting_for_data)) {
            parsing_completed = true;
          }
        }
      }

      if (current_char=='\0') {
        parsing_completed = true;
      }
      i++;
    }

    return s.toFloat();
}

//______________________________ SPI functions ______________________________

//___ Delay µs
void Delayus(unsigned int t)
{
unsigned int j;

for(j= 0; j < t; j++)   //loop ~1µs (for 328 at 16 MHz)
  {
  asm("nop");
  asm("nop");
  asm("nop");
  asm("nop");
  asm("nop");
  asm("nop");
  asm("nop");
  asm("nop");
  asm("nop");
  asm("nop");
  }
}

//___SPI init
#define SCK   PB5
#define MOSI  PB3
#define SS    PB2

#define SCK_HIGH PORTB|= (1 << SCK)           //set SCK to high
#define SCK_LOW PORTB&= ~(1 << SCK)           //set SCK to low

#define MOSI_HIGH PORTB|= (1 << MOSI)         //set MOSI to high
#define MOSI_LOW PORTB&= ~(1 << MOSI)         //set MOSI to low

#define SS_HIGH PORTB|= (1 << SS)           //set SS to high
#define SS_LOW PORTB&= ~(1 << SS)           //set SS to low

//__________ Init SPI interface
void SPI_MasterInit(void)
{
DDRB|= (1 << MOSI) | (1 << SCK) | (1 << SS);      //set MOSI, SCK and SS as output
SS_HIGH;
SCK_HIGH;
}

//__________ SPI master transfer (make in code C because µC SCK frequency is too hight for the display)
void SPI_MasterTransfer(char data)
{
int i;

SS_LOW;
for(i= 0; i < 8; i++)     //send data
  {
  Delayus(50);
  SCK_LOW;
  if(data & 0b10000000)
    {
    MOSI_HIGH;
    } 
  else
    {
    MOSI_LOW;
    }
  Delayus(50);
  SCK_HIGH;
  data= data << 1;
  }

Delayus(50);
SS_HIGH;
Delayus(110);
}

//__________ Sending string of characters with EOS (not used)
void SPI_StrSend(char *s)
{
LCDSPI_Clear();

SPI_MasterTransfer(0xFE);
SPI_MasterTransfer(0x53);           //Set backlight brightness
SPI_MasterTransfer(BACKLIGHT + 1);  //value of brightness

do
  {
  SPI_MasterTransfer(*s++);
  }
while(*(s-1));
}

//__________ Display string with her length specified
void LCDSPI_String(char *str, int lng)
{
char *p= str;

while(*p && (p - str) < lng)              //sendind string
  {
  if(*p >= ' ') SPI_MasterTransfer(*p);     //control codes filtering
  p++;
  }
}

//__________ Screen displaying
void Display_2x16(bool clear, char *s)
{
SPI_MasterTransfer(0xFE);
SPI_MasterTransfer(0x53);                 //Set backlight brightness
SPI_MasterTransfer((char)(BACKLIGHT + 1));  //value of brightness (+1 because brightness param of display begin to 1)
if(clear) LCDSPI_Clear();

SPI_MasterTransfer(0xFE);
SPI_MasterTransfer(0x45);           //set cursor
SPI_MasterTransfer(0x00);           //in line 1

LCDSPI_String(s, LNG_LINE);         //sendind first line

SPI_MasterTransfer(0xFE);
SPI_MasterTransfer(0x45);           //set cursor
SPI_MasterTransfer(0x40);           //in line 2

LCDSPI_String(s + LNG_LINE, LNG_LINE);    //sendind second line
}

//__________ Clear Screen
void LCDSPI_Clear(void)
{
SPI_MasterTransfer(0xFE);
SPI_MasterTransfer(0x51);           //display clear, cursor in line 1
Delayus(2000);
}
