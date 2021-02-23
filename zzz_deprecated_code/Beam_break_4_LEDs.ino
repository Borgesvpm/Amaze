/* Use a photoresistor (or photocell) to turn on an LED in the dark
   More info and circuit schematic: http://www.ardumotive.com/how-to-use-a-photoresistor-en.html
   Dev: Michalis Vasilakis // Date: 8/6/2015 // www.ardumotive.com */

//Constants
const int pResistor1 = A0; // Photoresistor at Arduino analog pin A0
const int ledPin1 = 5;     // Led pin at Arduino pin 5

const int pResistor2 = A1; // Photoresistor at Arduino analog pin A1
const int ledPin2 = 7;     // Led pin at Arduino pin 7

const int pResistor3 = A2; // Photoresistor at Arduino analog pin A2
const int ledPin3 = 9;     // Led pin at Arduino pin 9

const int pResistor4 = A3; // Photoresistor at Arduino analog pin A3
const int ledPin4 = 11;     // Led pin at Arduino pin 11



//Variables
int value1;          // Store value from photoresistor 1
int INIT_READ1;      // Store initial value from photoresistor 1

int value2;          // Store value from photoresistor 2
int INIT_READ2;      // Store initial value from photoresistor 2

int value3;          // Store value from photoresistor 3
int INIT_READ3;      // Store initial value from photoresistor 3

int value4;          // Store value from photoresistor 4
int INIT_READ4;      // Store initial value from photoresistor 4


void setup() {
  Serial.begin(9600);           //  setup serial
  pinMode(ledPin1, OUTPUT);  // Set lepPin - 5 pin as an output
  pinMode(pResistor1, INPUT);// Set pResistor - A0 pin as an input (optional)

  delay(50);
  INIT_READ1 = analogRead(pResistor1);
  delay(50);

  Serial.begin(9600);           //  setup serial
  pinMode(ledPin2, OUTPUT);  // Set lepPin - 7 pin as an output
  pinMode(pResistor2, INPUT);// Set pResistor - A1 pin as an input (optional)

  delay(50);
  INIT_READ2 = analogRead(pResistor2);
  delay(50);

  Serial.begin(9600);           //  setup serial
  pinMode(ledPin3, OUTPUT);  // Set lepPin - 9 pin as an output
  pinMode(pResistor3, INPUT);// Set pResistor - A2 pin as an input (optional)

  delay(50);
  INIT_READ3 = analogRead(pResistor3);
  delay(50);

  Serial.begin(9600);           //  setup serial
  pinMode(ledPin4, OUTPUT);  // Set lepPin - 11 pin as an output
  pinMode(pResistor4, INPUT);// Set pResistor - A3 pin as an input (optional)

  delay(50);
  INIT_READ4 = analogRead(pResistor4);
  delay(50);
}

void loop() {

  value1 = analogRead(pResistor1);
  //Serial.println(INIT_READ1);          // debug value
  if (value1 < INIT_READ1 - 20) {   // need to adjust this based on ambient light
    // animal is passing by
    // TO DO - Send signal to pi
    digitalWrite(ledPin1, LOW);  //Turn led off
  }
  else {
    digitalWrite(ledPin1, HIGH); //Turn led on
  }

  delay(50); //Small delay

  value2 = analogRead(pResistor2);
  //Serial.println(INIT_READ2);          // debug value
  Serial.println(value2);
  if (value2 < INIT_READ2 + 20) {   // need to adjust this based on ambient light
    // animal is passing by
    // TO DO - Send signal to pi
    digitalWrite(ledPin2, LOW);  //Turn led off
  }
  else {
    digitalWrite(ledPin2, HIGH); //Turn led on
  }

  delay(50); //Small delay

  value3 = analogRead(pResistor3);
  Serial.println(value3);          // debug value
  if (value3 < INIT_READ3 - 20) {   // need to adjust this based on ambient light
    // animal is passing by
    // TO DO - Send signal to pi
    digitalWrite(ledPin3, LOW);  //Turn led off
  }
  else {
    digitalWrite(ledPin3, HIGH); //Turn led on
  }

  delay(50); //Small delay

  value4 = analogRead(pResistor4);
  Serial.println(value4);          // debug value
  if (value4 < INIT_READ4 - 20) {   // need to adjust this based on ambient light
    // animal is passing by
    // TO DO - Send signal to pi
    digitalWrite(ledPin4, LOW);  //Turn led off
  }
  else {
    digitalWrite(ledPin4, HIGH); //Turn led on
  }

  delay(50); //Small delay
}
