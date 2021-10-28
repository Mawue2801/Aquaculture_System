  #include "DHT.h"
#define Type DHT11
int sensePin=2;
DHT HT(sensePin,Type);
float humidity;
float dhtTemp;
int setTime=500;
int dt=1000;
const int LDR1=A0;
const int LDR2=A2;
const int tempSensor=A1;
float LDR1Val;
float LDR2Val;
float tempVal;
int trigPin=4;
int echoPin=5;
int pingTravelTime;
float pingTravelDistance;
float distanceToTarget;
int redLED = 8;
int blueLED = 9;
int greenLED = 10;
char command;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(tempSensor,INPUT);
pinMode(LDR1,INPUT);
pinMode(LDR2,INPUT);
pinMode(trigPin,OUTPUT);
pinMode(echoPin,INPUT);
pinMode(redLED, OUTPUT);
pinMode(blueLED, OUTPUT);
pinMode(greenLED, OUTPUT);
HT.begin();
delay(setTime);
}
 
void loop() {
LDR1Val = (analogRead(LDR1) * 5) /1023;
LDR2Val = (analogRead(LDR2) * 5) /1023;
tempVal = (analogRead(tempSensor) * 500) / 1023;
humidity= HT.readHumidity();
dhtTemp = HT.readTemperature();
digitalWrite(trigPin,LOW);
delayMicroseconds(10);
digitalWrite(trigPin,HIGH);
delayMicroseconds(10);
digitalWrite(trigPin,LOW);
pingTravelTime=pulseIn(echoPin,HIGH);
pingTravelDistance=(pingTravelTime*765.*5280.*12)/(3600.*1000000);
distanceToTarget=(pingTravelDistance*0.0254)/2;


//Serial.print("LDR1: ");
//Serial.print(LDR1Val);
//Serial.print(",");
//Serial.print(" Temperature: ");
//Serial.print(tempVal);
//Serial.print(",");
//Serial.print(" Humidity: ");
//Serial.print(humidity);
//Serial.print(",");
//Serial.print(" DHT Temperature: ");
//Serial.print(dhtTemp);
//Serial.print(",");
//Serial.print(" Distance to Target is: ");
Serial.println(distanceToTarget);
//Serial.print(" in.");
//Serial.print(",");
//Serial.print(" LDR2: ");
//Serial.print(LDR2Val);

//Serial.print(";");

//Serial.print("LDR1: ");
//Serial.print(LDR1Val);
//Serial.print(",");
//Serial.print(" LDR2: ");
//Serial.print(LDR2Val);
//Serial.print(",");
//Serial.print(" Humidity: ");
//Serial.print(humidity);
//Serial.print(",");
//Serial.print(" DHT Temperature: ");
//Serial.print(dhtTemp);
//Serial.print(",");
//Serial.print(" Distance to Target is: ");
//Serial.print(distanceToTarget);
//Serial.print(" in.");
//Serial.print(",");
//Serial.print(" Temperature: ");
//Serial.println(tempVal);

if (Serial.available() > 0){
  command = Serial.read();
  if (command == 'R'){
    digitalWrite(redLED,HIGH);
  }
  if (command == 'B'){
    digitalWrite(blueLED,HIGH);
  }
  if (command == 'G'){
    digitalWrite(greenLED,HIGH);
  }
  if (command == 'r'){
    digitalWrite(redLED,LOW);
  }
}

delay(dt);
}
