
//set up leds, sensors

const int interval=500;//wait time from detection to catapult in ms
const int iti=1000;//intertrial interval
const int sensor_threshold=500; //incoming digital signal from raspberry is thresholded here

const int a1SensorPin=A1; //used to be a beam break sensor, now connected to raspberry digital out
int a1SensorValue=0;
int flag=0;
int trial=1;
int angle1=10;
int angle2=135;

#include<Servo.h>
Servo myServo1;

void setup() {
//led
 pinMode(3,OUTPUT);
 digitalWrite(3,HIGH); //drive voltage for led in a beam break (not connected today)
//sensor
a1SensorValue=analogRead(a1SensorPin); //analog value (used to be beam break sensor's photoresistor)

//servos
myServo1.attach(8); //social port
Serial.begin(9600);
myServo1.write(angle1);
delay(15);

//BNCs
pinMode(4,OUTPUT);
digitalWrite(4, LOW);
pinMode(2,OUTPUT);
digitalWrite(2, LOW);
//talk to PC
Serial.begin(9600);
}

void loop() {

digitalWrite(2, LOW);//start position

a1SensorValue=analogRead(a1SensorPin);
delay(1);
Serial.println(a1SensorValue);
 blocked by animal
Serial.println("enter trial");
digitalWrite(4, HIGH);//door open
myServo1.write(angle2);
delay(15);
flag=2;
}
}
if (flag>1){
Serial.println("animal at social, waiting ");
delay(interval);
digitalWrite(2, HIGH);//catapult
Serial.println("catapult deployed");
flag=0;
delay(interval);
myServo1.write(angle1);
delay(15);
digitalWrite(4, LOW);//door close
delay(iti);
trial=trial+1;
Serial.print("TRIAL primed ");
Serial.println(trial);
}

}
