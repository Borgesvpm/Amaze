/* Use a photoresistor (or photocell) to turn on an LED in the dark
   More info and circuit schematic: http://www.ardumotive.com/how-to-use-a-photoresistor-en.html
   Dev: Michalis Vasilakis // Date: 8/6/2015 // www.ardumotive.com */

#include<Servo.h>
Servo servo1;     // Servo 1
 
//Constants
const int pResistor1 = A0; // Photoresistor at Arduino analog pin A0
const int ledPin1 = 2;      // Led pin at Arduino pin 2
const int servoPin1 = 3;      // control servo
const int PiPin1 = 4;      // send report to Pi
const int CLOSE_DOOR = 10;      // Angle of 10 degrees -> door is closed
const int OPEN_DOOR = 135;     // Angle of 135 degrees -> door is opened
const int PiInPin = 0;  


//Variables
int photo_value1;          // Store value from photoresistor (0-1023)
int INIT_READ1;    // Store initial value from photoresistor    
int START; 
int FLAG1;   
int FLAG2;   
int FLAG3;   

void setup(){
  Serial.begin(9600);           //  setup serial
  pinMode(ledPin1, OUTPUT);  // Set ledPin - 2 pin as an output
  pinMode(pResistor1, INPUT);// Set pResistor - A0 pin as an input (optional)
  pinMode(PiPin1, OUTPUT);  
  pinMode(PiInPin, INPUT);// input commands from Pi
  
  delay(50);
  INIT_READ1 = analogRead(pResistor1);
  delay(50);

servo1.attach(servoPin1);
  //servos
  servo1.write(CLOSE_DOOR);
  delay(15);
  digitalWrite(PiPin1, LOW);//communication to Pi
  digitalWrite(ledPin1, HIGH); //Turn led on

 START=LOW; //initialize start signal
 FLAG1=0;   //initialize flags
 FLAG2=1;  
 FLAG3=1;  
 
}

void loop(){

//start waiting for flags from Pi
START=digitalRead(PiInPin);


if (START = HIGH){

 if (FLAG1<1){

      servo1.write(OPEN_DOOR);
    delay(15);

  photo_value1 = analogRead(pResistor1);
  Serial.println(photo_value1);          // debug value
  if (photo_value1 < INIT_READ1 - 50){    // values needs to be adjusted this based on ambient light
    // animal is passing by
    // TO DO - Send signal to pi
    digitalWrite(ledPin1, LOW);  //Turn led off
    servo1.write(CLOSE_DOOR);
    delay(15);
    digitalWrite(PiPin1, HIGH);//pulse to Pi to start scale and move on.
    FLAG1=1; FLAG2=0; FLAG3=1;
  }
 }
 if (FLAG2<1) {
 //ADD CODE HERE FOR NEXT INSTANCE
  FLAG1=1; FLAG2=1;FLAG3=0;
 }
  if (FLAG3<1) {
 //ADD CODE HERE FOR MAZE
  FLAG1=1; FLAG2=1;FLAG3=1;
 }
 
}//start loop end

  
}//void loop end
