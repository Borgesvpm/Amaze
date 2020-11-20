#include<Servo.h>
Servo servo1;     // Servo 1
#include<Servo.h>
Servo servo2;     
#include<Servo.h>
Servo servo3;     
#include<Servo.h>
Servo servo4;     
 
//Constants
const int pResistor1 = A0; // Photoresistors A0-A3
const int pResistor2 = A1; 
const int pResistor3 = A2; 
const int pResistor4 = A3; 

// pins 2 and 3 are reserved for interrupt

const int servoPin1 = 4;      // control servos 1-3
const int servoPin2 = 5;
const int servoPin3 = 6;
const int servoPin4 = 7;// control brake servo in running wheel

const int ard_pi_1 = 8;      // send reports to Pi 
const int ard_pi_2 = 9; 
const int ard_pi_3 = 10;
const int ard_pi_4 = 11;  

const int pi_RFID = 12;      // receive RFID command from Pi 
const int pi_scale = 13;       // receive weight decision from Pi

const int CLOSE_DOOR1 = 135;      // Angle of 135 degrees -> door is closed
const int OPEN_DOOR1 = 20;     // Angle of 20 degrees -> door is opened
const int CLOSE_DOOR2 = 155;      // Angle of 155 degrees -> door is closed
const int OPEN_DOOR2 = 20;        // 20
const int CLOSE_DOOR3 = 159;      // Angle of 157 degrees -> middle passage is closed
const int OPEN_DOOR3 = 87;        // 89
const int RELEASE_WHEEL = 100;      // Angle of 100 degrees -> WHEEL is free
const int BRAKE_WHEEL = 20;  //20 CLAMPED

//Variables
int beam_breaker_scale;          // Store value from photoresistor (0-1023)
int INIT_BB_SCALE;                  // Store initial value from photoresistor    
int beam_breaker_middle;          // Store value from photoresistor (0-1023)
int INIT_BB_MIDDLE;
int beam_breaker_task;          // Store value from photoresistor (0-1023)
int INIT_BB_TASK;
int beam_breaker_homecage;          // Store value from photoresistor (0-1023)
int INIT_BB_HOMECAGE;
int pi_RFID_trig; 
int pi_scale_trig;
int START;
int MODE;   
long interval = 3000; 

void setup(){
  Serial.begin(9600);           //  setup serial
  pinMode(pResistor1, INPUT);// Set pResistor - A0 pin as an input 
  pinMode(pResistor2, INPUT);
  pinMode(pResistor3, INPUT);
  pinMode(pResistor4, INPUT);
  pinMode(pi_RFID, INPUT);// input commands from Pi
  pinMode(pi_scale, INPUT);
  pinMode(ard_pi_1, OUTPUT);  //output reports to Pi
  pinMode(ard_pi_2, OUTPUT);  
  pinMode(ard_pi_3, OUTPUT); 
  pinMode(ard_pi_4, OUTPUT); 

  digitalWrite(ard_pi_1, LOW);//communication to Pi
  digitalWrite(ard_pi_2, LOW);
  digitalWrite(ard_pi_3, LOW);
  digitalWrite(ard_pi_4, LOW);
 
 MODE=1;   //initialize MODE flag
 START = LOW;

  INIT_BB_SCALE = analogRead(pResistor1);
  INIT_BB_MIDDLE = analogRead(pResistor2);
  INIT_BB_TASK = analogRead(pResistor3);
  INIT_BB_HOMECAGE = analogRead(pResistor4);

   Serial.print("INIT_BB_SCALE ");  
 Serial.println(INIT_BB_SCALE);  
   Serial.print("INIT_BB_MIDDLE ");  
 Serial.println(INIT_BB_MIDDLE);  
    Serial.print("INIT_BB_TASK ");  
 Serial.println(INIT_BB_TASK);  
    Serial.print("INIT_BB_HOMECAGE ");  
 Serial.println(INIT_BB_HOMECAGE);  

servo1.attach(servoPin1);
  servo1.write(CLOSE_DOOR1);
servo2.attach(servoPin2);
  servo2.write(CLOSE_DOOR2);
servo3.attach(servoPin3);
  servo3.write(OPEN_DOOR3);
servo4.attach(servoPin4);
  servo4.write(RELEASE_WHEEL);

}

void loop(){
//  // Troubleshooting code
//beam_breaker_scale = analogRead(pResistor1);
//beam_breaker_middle = analogRead(pResistor2);
//beam_breaker_task = analogRead(pResistor3);
//beam_breaker_homecage = analogRead(pResistor4);
//Serial.print("MODE IS "); 
//Serial.println(MODE); 
// Serial.print("beam_breaker_scale ");  
// Serial.println(beam_breaker_scale);  
// Serial.print("beam_breaker_middle ");  
// Serial.println(beam_breaker_middle);  
//  Serial.print("beam_breaker_task ");  
// Serial.println(beam_breaker_task);  
// Serial.print("beam_breaker_homecage ");  
// Serial.println(beam_breaker_homecage);  

//MODE flag based state machine, that waits in MODEs 1 and 2 for a START signal from Pi
//MODEs 3 and 4 are T-maze modes that do not need Pi, they only send info to Pi about when beam-breaks were triggered

pi_RFID_trig = digitalRead(pi_RFID);
pi_scale_trig = digitalRead(pi_scale);
Serial.println(pi_RFID_trig); 
Serial.println(pi_scale_trig);
Serial.println(ard_pi_1);

//START=digitalRead(pi_ard_1);
   if (beam_breaker_task < INIT_BB_TASK - 50){    // use reward beam as trig signal for setting up without Pi
    Serial.println("trig"); 
    START=HIGH; 
  }

if (MODE==1){ //home cage
  if (pi_RFID_trig == 1){
    servo1.write(OPEN_DOOR1);
    START=HIGH;
    
  beam_breaker_scale = analogRead(pResistor1);
  if (beam_breaker_scale < (0.9 * INIT_BB_SCALE) ){    // values needs to be adjusted based on ambient light
    Serial.println("animal in scale"); 
    digitalWrite(ard_pi_1, HIGH);//pulse to Pi to start scale
    digitalWrite(ard_pi_2, HIGH);
    digitalWrite(ard_pi_3, HIGH);
    digitalWrite(ard_pi_4, HIGH);
    Serial.println("sent ard_pi_1 pulse to Pi");
    servo1.write(CLOSE_DOOR1);
    MODE=2;//end state can flag movement to other states
    START=LOW;
  }}}

if (MODE==2){ //scale
if (pi_scale_trig == 1){
      servo2.write(OPEN_DOOR2);
    delay(20000);
}
  beam_breaker_middle = analogRead(pResistor2);
  if (beam_breaker_middle < (0.9 * INIT_BB_MIDDLE) ){    // values needs to be adjusted based on ambient light
    Serial.println("enter maze"); 

    digitalWrite(ard_pi_2, HIGH);//pulse to Pi to say maze is active.
    MODE=3;//end state can flag movement to other states
    START=LOW;
  }}

if (MODE==3){ 
  
  //maze start scenario
  INIT_BB_TASK = analogRead(pResistor3);
  if (INIT_BB_TASK < INIT_BB_TASK - 50){    // values needs to be adjusted based on ambient light
    Serial.println("enter pod"); 
    servo3.write(CLOSE_DOOR3);
    delay(1000);
    digitalWrite(ard_pi_3, HIGH);//pulse to Pi to say maze is active.
    MODE=3;//end state can flag movement to other states
    START=LOW; 
  }

  //maze new trial scenario
  INIT_BB_MIDDLE = analogRead(pResistor2);
  if (INIT_BB_MIDDLE < INIT_BB_MIDDLE - 50){    // values needs to be adjusted based on ambient light
    Serial.println("new trial available"); 
      servo3.write(OPEN_DOOR3);
    delay(100);
    digitalWrite(ard_pi_2, HIGH);//pulse to Pi .
  }

  //maze exit scenario
  INIT_BB_SCALE = analogRead(pResistor1);
  if (INIT_BB_SCALE < INIT_BB_SCALE - 50){    
      Serial.println("animal wants out"); 
      servo2.write(CLOSE_DOOR2);
      delay(100);
      MODE=4;
  }
  }

   if (MODE==4){ 
     //going back to cage
     INIT_BB_SCALE = analogRead(pResistor1);
  if (INIT_BB_SCALE < INIT_BB_SCALE - 50){    // values needs to be adjusted based on ambient light
     servo1.write(OPEN_DOOR1);
}
if (INIT_BB_HOMECAGE < INIT_BB_HOMECAGE - 10){    // values needs to be adjusted based on ambient light
     servo1.write(CLOSE_DOOR1);
        MODE=1;
   }
   }
}//void loop end
