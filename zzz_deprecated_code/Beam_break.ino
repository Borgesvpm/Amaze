/* Use a photoresistor (or photocell) to turn on an LED in the dark
   More info and circuit schematic: http://www.ardumotive.com/how-to-use-a-photoresistor-en.html
   Dev: Michalis Vasilakis // Date: 8/6/2015 // www.ardumotive.com */
   
//Constants
const int pResistor = A0; // Photoresistor at Arduino analog pin A0
const int ledPin=7;       // Led pin at Arduino pin 9

//Variables
int value;          // Store value from photoresistor (0-1023)
int INIT_READ;      // Store initial value from photoresistor



void setup(){
  Serial.begin(9600);           //  setup serial
  pinMode(ledPin, OUTPUT);  // Set lepPin - 9 pin as an output
  pinMode(pResistor, INPUT);// Set pResistor - A0 pin as an input (optional)
  
  delay(50);
  INIT_READ = analogRead(pResistor);
  delay(50);
}

void loop(){

  value = analogRead(pResistor);
  Serial.println(value);          // debug value
  if (value < INIT_READ - 20){    // need to adjust this based on ambient light
    // animal is passing by
    // TO DO - Send signal to pi
    digitalWrite(ledPin, LOW);  //Turn led off
  }
  else{
    digitalWrite(ledPin, HIGH); //Turn led on
  }

  delay(50); //Small delay
}
