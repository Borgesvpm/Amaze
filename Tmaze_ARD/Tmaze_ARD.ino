
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

const int servoPin1 = 2;      // control servos 1-3
const int servoPin2 = 3;
const int servoPin3 = 4;
const int servoPin4 = 5;// control brake servo in running wheel

const int ard_pi_1 = 8;      // send reports to Pi 
const int ard_pi_2 = 9; 
const int ard_pi_3 = 10;
const int ard_pi_4 = 11;  

const int CLOSE_DOOR1 = 135;      // Angle of 135 degrees -> door is closed
const int OPEN_DOOR1 = 20;     // Angle of 20 degrees -> door is opened
const int CLOSE_DOOR2 = 155;      // Angle of 155 degrees -> door is closed
const int OPEN_DOOR2 = 20;        // 20
const int CLOSE_DOOR3 = 159;      // Angle of 157 degrees -> middle passage is closed
const int OPEN_DOOR3 = 87;        // 89
const int RELEASE_WHEEL = 100;      // Angle of 100 degrees -> WHEEL is free
const int BRAKE_WHEEL = 20;  //20 CLAMPED

const int pi_ard_1 = 12;      // receive RFID command from Pi 
const int pi_ard_2 = 13;       // receive weight decision from Pi


//Variables
int photo_value1;          // Store value from photoresistor (0-1023)
int INIT_READ1;    // Store initial value from photoresistor    
int photo_value2;          // Store value from photoresistor (0-1023)
int INIT_READ2;
int photo_value3;          // Store value from photoresistor (0-1023)
int INIT_READ3;
int photo_value4;          // Store value from photoresistor (0-1023)
int INIT_READ4;
int START; 
int MODE;   
long interval = 3000; 

void setup(){
  Serial.begin(9600);           //  setup serial
  pinMode(pResistor1, INPUT);// Set pResistor - A0 pin as an input 
  pinMode(pResistor2, INPUT);
  pinMode(pResistor3, INPUT);
  pinMode(pResistor4, INPUT);
  pinMode(ard_pi_1, OUTPUT);  //output reports to Pi
  pinMode(ard_pi_2, OUTPUT);  
  pinMode(ard_pi_3, OUTPUT); 
  pinMode(ard_pi_4, OUTPUT); 
  pinMode(pi_ard_1, INPUT);// input commands from Pi
  pinMode(pi_ard_2, INPUT);
    


servo1.attach(servoPin1);
  servo1.write(OPEN_DOOR1);
  delay(1000);
  servo1.write(CLOSE_DOOR1);
  delay(1000);
servo2.attach(servoPin2);
  servo2.write(OPEN_DOOR2);
  delay(1000);
  servo2.write(CLOSE_DOOR2);
  delay(1000);
  servo3.attach(servoPin3);
  servo3.write(CLOSE_DOOR3);
  delay(1000);
  servo3.write(OPEN_DOOR3);
  delay(1000);
  servo4.attach(servoPin4);
  servo4.write(BRAKE_WHEEL);
  delay(1000);
  servo4.write(RELEASE_WHEEL);
  delay(1000);
  
  digitalWrite(ard_pi_1, LOW);//communication to Pi
  digitalWrite(ard_pi_2, LOW);
  digitalWrite(ard_pi_3, LOW);
  digitalWrite(ard_pi_4, LOW);

 START=LOW; //initialize start signal
 MODE=1;   //initialize MODE flag


  INIT_READ1 = analogRead(pResistor1);
  INIT_READ2 = analogRead(pResistor2);
  INIT_READ3 = analogRead(pResistor3);
  INIT_READ4 = analogRead(pResistor4);

   Serial.print("INIT_READ1 ");  
 Serial.println(INIT_READ1);  
   Serial.print("INIT_READ2 ");  
 Serial.println(INIT_READ2);  
    Serial.print("INIT_READ3 ");  
 Serial.println(INIT_READ3);  
    Serial.print("INIT_READ4 ");  
 Serial.println(INIT_READ4);  

  
}

void loop(){
photo_value1 = analogRead(pResistor1);
photo_value2 = analogRead(pResistor2);
photo_value3 = analogRead(pResistor3);
photo_value4 = analogRead(pResistor4);
Serial.print("MODE IS "); 
Serial.println(MODE); 
 Serial.print("photo_value1 ");  
 Serial.println(photo_value1);  
 Serial.print("photo_value2 ");  
 Serial.println(photo_value2);  
  Serial.print("photo_value3 ");  
 Serial.println(photo_value3);  
 Serial.print("photo_value4 ");  
 Serial.println(photo_value4);  



//MODE flag based state machine, that waits in MODEs 1 and 2 for a START signal from Pi
//MODEs 3 and 4 are T-maze modes that do not need Pi, they only send info to Pi about when beam-breaks were triggered


START=digitalRead(pi_ard_1);
//   if (photo_value3 < INIT_READ3 - 50){    // use reward beam as trig signal for setting up without Pi
//    Serial.println("trig"); 
//    START=HIGH; 
//  }

if (MODE==1){ //home cage
if (START == 1){
      servo1.write(OPEN_DOOR1);
    delay(100);
  photo_value1 = analogRead(pResistor1);
  if (photo_value1 < INIT_READ1 - 50){    // values needs to be adjusted based on ambient light
    Serial.println("animal in scale"); 
    servo1.write(CLOSE_DOOR1);
    delay(1000);
    digitalWrite(ard_pi_1, HIGH);//pulse to Pi to start scale and move on.
    MODE=2;//end state can flag movement to other states
    START=LOW; 
  }}}

if (MODE==2){ //scale
if (START == 1){
      servo2.write(OPEN_DOOR2);
    delay(100);
}
  photo_value2 = analogRead(pResistor2);
  if (photo_value2 < INIT_READ2 - 50){    // values needs to be adjusted based on ambient light
    Serial.println("enter maze"); 

    digitalWrite(ard_pi_2, HIGH);//pulse to Pi to say maze is active.
    MODE=3;//end state can flag movement to other states
    START=LOW; 
  }}

if (MODE==3){ 
  
  //maze start scenario
  photo_value3 = analogRead(pResistor3);
  if (photo_value3 < INIT_READ3 - 50){    // values needs to be adjusted based on ambient light
    Serial.println("enter pod"); 
    servo3.write(CLOSE_DOOR3);
    delay(1000);
    digitalWrite(ard_pi_3, HIGH);//pulse to Pi to say maze is active.
    MODE=3;//end state can flag movement to other states
    START=LOW; 
  }

  //maze new trial scenario
  photo_value2 = analogRead(pResistor2);
  if (photo_value2 < INIT_READ2 - 50){    // values needs to be adjusted based on ambient light
    Serial.println("new trial available"); 
      servo3.write(OPEN_DOOR3);
    delay(100);
    digitalWrite(ard_pi_2, HIGH);//pulse to Pi .
  }

  //maze exit scenario
  photo_value1 = analogRead(pResistor1);
  if (photo_value1 < INIT_READ1 - 50){    
      Serial.println("animal wants out"); 
      servo2.write(CLOSE_DOOR2);
      delay(100);
      MODE=4;
  }
  }

   if (MODE==4){ 
     //going back to cage
     photo_value1 = analogRead(pResistor1);
  if (photo_value1 < INIT_READ1 - 50){    // values needs to be adjusted based on ambient light
     servo1.write(OPEN_DOOR1);
}
if (photo_value4 < INIT_READ4 - 10){    // values needs to be adjusted based on ambient light
     servo1.write(CLOSE_DOOR1);
        MODE=1;
   }
   }
}//void loop end
