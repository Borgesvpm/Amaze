#include<Servo.h>
Servo servo1;     // Servo 1 = door1
#include<Servo.h>
Servo servo2;     // Servo 2 = door2
#include<Servo.h>
Servo servo3;     // Servo 3 = door3
#include<Servo.h>
Servo servo4;     // Servo 4 = running-wheel brake
#include<Servo.h>
Servo servo5;     // Servo 5 = food pod
 
//Constants
long interval = 60000; //CHANGE THIS TO CHANGE POD TIMING
const int pResistor1 = A0; // BB1
const int pResistor2 = A1; // BB2
const int pResistor3 = A2; //BB4 choice running wheel
const int pResistor4 = A3; // BB5
const int pResistor5 = A4; //BB3 choice food pod

const int servoPin1 = 4;      // control servos 1-3
const int servoPin2 = 5;
const int servoPin3 = 6;
const int servoPin4 = 7;// control brake servo in running wheel
const int servoPin5 = 3;// control food servo in hunting chamber

const int ard_pi_1 = 8;      // reports MODE=2 to Pi 
const int ard_pi_2 = 9;     // reports trial start to Pi
const int ard_pi_3 = 10;  // reports MODE=1 to Pi
const int ard_pi_4 = 11;  // reports food pod entry to Pi
const int ard_pi_5 = 2;  // reports running wheel pod entry to Pi

const int CLOSE_DOOR1 = 135;      // Angle of 135 degrees -> door is closed
const int OPEN_DOOR1 = 30;     // Angle of 20 degrees -> door is opened
const int CLOSE_DOOR2 = 155;      // Angle of 155 degrees -> door is closed
const int OPEN_DOOR2 = 20;        // 20
const int CLOSE_DOOR3 = 159;      // Angle of 157 degrees -> middle passage is closed
const int OPEN_DOOR3 = 87;        // 89
const int RELEASE_WHEEL = 100;      // Angle of 100 degrees -> WHEEL is free
const int BRAKE_WHEEL = 20;  //20 CLAMPED
const int SHOW_FOOD = 170;      // Angle of 120 degrees -> FOOD IN CENTER
const int HIDE_FOOD = 123;  //175 HIDDEN

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
int photo_value5;          // Store value from photoresistor (0-1023)
int INIT_READ5;
int START=LOW; //initialize start signal
int MODE=1;   //initialize MODE

int pos = 0; //generic servo pos variable for use in blocking for-loops for semi-slow motion (keep to less than 500ms total and ensure no arduino detector events can happen during this)
int pos5 = 0; //food pod servo angle needs to be updated within if statements for non-blocking slow movement, so depending on maze state it will be 'gravitating' toward open or closed at its own speed
int maze_mode = 1; //initialize maze mode (1=open rewards, 2=countdown timer, 3=close rewards)
int flag = 0; //initialize flag in maze (0 for start side, 1 for reward side)
unsigned long tic = 0;
unsigned long duration = 0; 
unsigned long tic2 = 0;
unsigned long duration2 = 0; 
int time_flag=0;//timer flags 0,1 used in short if staments that remove themselves so first time point is not measured on subsequent loops
int time_flag2=0;
int time_flag3=0;

void setup(){
  Serial.begin(9600);           //  setup serial
  pinMode(pResistor1, INPUT);// Set pResistor - A0 pin as an input 
  pinMode(pResistor2, INPUT);
  pinMode(pResistor3, INPUT);
  pinMode(pResistor4, INPUT);
  pinMode(pResistor5, INPUT);
  pinMode(ard_pi_1, OUTPUT);  //output reports to Pi
  pinMode(ard_pi_2, OUTPUT);  
  pinMode(ard_pi_3, OUTPUT); 
  pinMode(ard_pi_4, OUTPUT); 
  pinMode(ard_pi_5, OUTPUT); 
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
  servo3.attach(servoPin3); //for loops for slow servo movement
    for (pos = OPEN_DOOR3; pos <= CLOSE_DOOR3; pos += 1) { // close
    servo3.write(pos);     
    delay(8);                  
  }
  delay(1000);
  for (pos = CLOSE_DOOR3; pos >= OPEN_DOOR3; pos -= 1) { // open
    servo3.write(pos);           
    delay(7);                    
  }
delay(1000);
  servo4.attach(servoPin4);
  servo4.write(BRAKE_WHEEL);
  delay(1000);
  servo4.write(RELEASE_WHEEL);
  delay(1000);
    servo5.attach(servoPin5);  //for loops for slow servo movement
  for (pos5 = HIDE_FOOD; pos5 <= SHOW_FOOD; pos5 += 1) { // show food
    servo5.write(pos5);              
    delay(30);                  
  }
  delay(1000);
  for (pos5 = SHOW_FOOD; pos5 >= HIDE_FOOD; pos5 -= 1) { // hide food
    servo5.write(pos5);
    delay(30);
  }
  
  digitalWrite(ard_pi_1, LOW);//communication to Pi
  digitalWrite(ard_pi_2, LOW);
  digitalWrite(ard_pi_3, LOW);
  digitalWrite(ard_pi_4, LOW);
  digitalWrite(ard_pi_5, LOW);

  INIT_READ1 = analogRead(pResistor1); // calibrate beam-breaks
  INIT_READ2 = analogRead(pResistor2);
  INIT_READ3 = analogRead(pResistor3);
  INIT_READ4 = analogRead(pResistor4);
  INIT_READ5 = analogRead(pResistor5);
  
   Serial.print("INIT_READ1 ");  //show beam break values for trouble shooting if serial monitor is on
 Serial.println(INIT_READ1);  
   Serial.print("INIT_READ2 ");  
 Serial.println(INIT_READ2);  
    Serial.print("INIT_READ3 ");  
 Serial.println(INIT_READ3);  
    Serial.print("INIT_READ4 ");  
 Serial.println(INIT_READ4);  
    Serial.print("INIT_READ5 ");  
 Serial.println(INIT_READ5);  
      Serial.print("MODE IS "); 
Serial.println(MODE); 
}

void loop(){
photo_value1 = analogRead(pResistor1); //read beam breaks
photo_value2 = analogRead(pResistor2);
photo_value3 = analogRead(pResistor3);
photo_value4 = analogRead(pResistor4);
photo_value5 = analogRead(pResistor5);
// Serial.print("photo_value1 ");  
// Serial.println(photo_value1);  
// Serial.print("photo_value2 ");  
// Serial.println(photo_value2);  
//  Serial.print("photo_value3 ");  
// Serial.println(photo_value3);  
// Serial.print("photo_value4 ");  
// Serial.println(photo_value4);  
// Serial.print("photo_value5 ");  
// Serial.println(photo_value5);  

//MODE flag based state machine, that waits in MODEs 1 and 2 for a START signal from Pi
//MODEs 3 and 4 are T-maze modes that do not need Pi, they only send info to Pi about when beam-breaks were triggered

START=digitalRead(pi_ard_1);//RFID INPUT from Pi

if (MODE==1){ //home cage
if (START == 1){
    servo1.write(OPEN_DOOR1);
    delay(100);
  photo_value1 = analogRead(pResistor1);
  if (photo_value1 < 0.8*INIT_READ1){    // BEAM BREAK DEFINITION. Factor can be adjusted based on ambient light.
    Serial.println("animal in scale"); 
    servo1.write(CLOSE_DOOR1); //trap animal in scale
    delay(100);
    digitalWrite(ard_pi_1, HIGH);//pulse to Pi to start reading scale and go MODE 2.
    delay(100);
    digitalWrite(ard_pi_1, LOW);//end pulse to Pi.
    MODE=2;//end state 
    Serial.print("MODE IS "); 
    Serial.println(MODE); 
    START=LOW; 
  }}}

if (MODE==2){ //scale
if (START == 1){ //Pi communicates weight recorded
    servo2.write(OPEN_DOOR2); //let animal out of scale into T-maze
    delay(10); //textbook delay after servo operation for capacitance charging
  }
  photo_value2 = analogRead(pResistor2); // reading BEAM BREAK 2 
  if (photo_value2 < 0.8*INIT_READ2){    // BEAM BREAK 2
    Serial.println("enter maze"); 
    digitalWrite(ard_pi_2, HIGH);//pulse to Pi to say maze is active.
    delay(100);
    digitalWrite(ard_pi_2, LOW);//end pulse to Pi.
    MODE=3;
    Serial.print("MODE IS "); 
    Serial.println(MODE); 
    START=LOW; 
  }}

if (MODE==3){ //Animal in T-maze deciding: food pod, running wheel or go home.
  // this mode uses 
  // flag=0,1 for (0=start side, 1=decision side)
  // maze_mode=1,2,3 for (1=open rewards, 2=countdown timer, 3=close rewards)
  
  //maze start scenario
  photo_value3 = analogRead(pResistor3);
  photo_value5 = analogRead(pResistor5);
  if (flag == 0){
  if (photo_value3 < 0.7*INIT_READ3){   //in run wheel pod
    flag = 1; maze_mode=1;time_flag=1;tic=millis();
    Serial.println("enter runwheel pod"); 
    digitalWrite(ard_pi_5, HIGH);//pulse to Pi to say runwheel pod entry.
    for (pos = OPEN_DOOR3; pos <= CLOSE_DOOR3; pos += 1) { // close
    servo3.write(pos);     
    delay(8);              
  }

    servo4.write(RELEASE_WHEEL);
  delay(10);
    digitalWrite(ard_pi_5, LOW);//end pulse to Pi.
  }
    if (photo_value5 < 0.7*INIT_READ5){   //in food pod
    flag = 1; maze_mode=1;time_flag=1;tic=millis();
    Serial.println("enter food pod"); 
    digitalWrite(ard_pi_4, HIGH);//pulse to Pi to say foodpod entry.
    for (pos = OPEN_DOOR3; pos <= CLOSE_DOOR3; pos += 1) { // close
    servo3.write(pos);     
    delay(8);              
  }
      servo4.write(RELEASE_WHEEL);
  delay(10);
    digitalWrite(ard_pi_4, LOW);//end pulse to Pi.
  }}

if (flag == 1){
  if (maze_mode==1){//non-blocking loop to move food to center without delays to code since animal could go elsewhere.
    if (time_flag==1){tic2=millis();time_flag=0;}
    if (pos5 < SHOW_FOOD){
    duration2=millis()-tic2;
if (duration2>30){
servo5.write(pos5); 
pos5=pos5+1;tic2=millis();
    }}
    }
    if (pos5 == SHOW_FOOD){
      maze_mode=2; pos5=SHOW_FOOD-1;time_flag2=1;
    }
  if (maze_mode==2){
    duration=millis()-tic;
//    Serial.print("duration is "); 
//    Serial.println(duration);
  }
  if (duration>interval){
    maze_mode=3;
    if (time_flag2==1){tic=millis();time_flag=1;time_flag2=0;time_flag3=1;}
  servo4.write(BRAKE_WHEEL);
  //non-blocking for loop to move food away without delays to code since animal could be elsewhere.
       if (time_flag==1){tic2=millis();time_flag=0;}
    if (pos5 > HIDE_FOOD){
    duration2=millis()-tic2;
if (duration2>30){
tic2=millis();
servo5.write(pos5); 
pos5=pos5-1;
    }}
  }}
  
    if (flag == 0){ //animal has passed to start side!
    duration=0;maze_mode=3;
    if (time_flag3==1){tic=millis();time_flag3=0;}
  servo4.write(BRAKE_WHEEL);
  //non-blocking for loop to move food away without delays to code since animal could be elsewhere.
    if (pos5 > HIDE_FOOD){
    duration=millis()-tic;
if (duration>30){
tic=millis();
servo5.write(pos5); 
pos5=pos5-1;
    }}
  }
  
  //maze new trial scenario
  photo_value2 = analogRead(pResistor2);
  if (flag == 1){
  if (photo_value2 < 0.8*INIT_READ2){   
    flag=0;
    Serial.println("trial"); 
    digitalWrite(ard_pi_2, HIGH);//pulse to Pi new trial
    for (pos = CLOSE_DOOR3; pos >= OPEN_DOOR3; pos -= 1) { // open
    servo3.write(pos);           
    delay(8);                    
  }
    digitalWrite(ard_pi_2, LOW);//end pulse to Pi
  }}

  //maze exit scenario
  photo_value1 = analogRead(pResistor1);
  if (photo_value1 < 0.8*INIT_READ1){    
      Serial.println("animal wants out"); 
      servo2.write(CLOSE_DOOR2);
      delay(100);
      MODE=4;
          Serial.print("MODE IS "); 
Serial.println(MODE); 
  }
  }

   if (MODE==4){ 
     //going back to cage
     servo1.write(OPEN_DOOR1);
if (photo_value4 < 0.8*INIT_READ4){    // values needs to be adjusted based on ambient light
     servo1.write(CLOSE_DOOR1);
     delay(100);
     digitalWrite(ard_pi_3, HIGH);//pulse to Pi to sync to MODE 1.
     delay(100);
     digitalWrite(ard_pi_3, LOW);//end pulse to Pi.
        MODE=1;
   }
   }
}//void loop end
