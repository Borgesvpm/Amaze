/* Use a photoresistor (or photocell) to turn on an LED in the dark
   More info and circuit schematic: http://www.ardumotive.com/how-to-use-a-photoresistor-en.html
   Dev: Michalis Vasilakis // Date: 8/6/2015 // www.ardumotive.com */

#include<Servo.h>
Servo servo1;     // Servo 1
 
//Constants
const int pResistor1 = A0; // Photoresistor at Arduino analog pin A0
const int ledPin1 = 2;      // Led pin at Arduino pin 2
const int CLOSE_DOOR = 10;      // Angle of 10 degrees -> door is closed
const int OPEN_DOOR = 135;     // Angle of 135 degrees -> door is opened

//Variables
int photo_value1;          // Store value from photoresistor (0-1023)
int INIT_READ1;      // Store initial value from photoresistor    

void setup(){
  Serial.begin(9600);           //  setup serial
  pinMode(ledPin1, OUTPUT);  // Set ledPin - 2 pin as an output
  pinMode(pResistor1, INPUT);// Set pResistor - A0 pin as an input (optional)
  
  delay(50);
  INIT_READ1 = analogRead(pResistor1);
  delay(50);

  //servos
  servo1.write(CLOSE_DOOR);
  delay(15);
}

void loop(){

  photo_value1 = analogRead(pResistor1);
  Serial.println(photo_value1);          // debug value
  if (photo_value1 < INIT_READ1 - 50){    // values needs to be adjusted this based on ambient light
    // animal is passing by
    // TO DO - Send signal to pi
    digitalWrite(ledPin1, LOW);  //Turn led off
    servo1.write(OPEN_DOOR);
    delay(3000); // wait 3 seconds (testing purposes)
    servo1.write(CLOSE_DOOR);
  }
  else{
    digitalWrite(ledPin1, HIGH); //Turn led on
  }

  delay(50); //Small delay
}
