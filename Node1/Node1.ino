/*
 Lora Node1
https://www.electroniclinic.com/

*/
#include <SPI.h>              // include libraries
#include <LoRa.h>
#include "DHT.h"
#define Type DHT11
int sensePin = 4;
DHT HT(sensePin,Type);
float humidity;
float dhtTemp;
//int setTime = 500;

int LED = 8; 

String outgoing;              // outgoing message

byte msgCount = 0;            // count of outgoing messages
byte MasterNode = 0xAA;     
byte Node1 = 0xBB;

unsigned long previousMillis=0;
unsigned long int previoussecs = 0; 
unsigned long int currentsecs = 0; 
unsigned long currentMillis = 0;

int interval = 1 ; // updated every 1 second
int Secs = 0; 
String message = "";


void setup() {
  Serial.begin(9600);                   // initialize serial
  pinMode(LED, OUTPUT);
  HT.begin();
  delay(500);
  
  //while (!Serial);

  Serial.println("LoRa Duplex");



  if (!LoRa.begin(915E6)) {             // initialize ratio at 915 MHz
    Serial.println("LoRa init failed. Check your connections.");
    while (true);                       // if failed, do nothing
  }

  Serial.println("LoRa init succeeded.");
}

void loop() {
   humidity= HT.readHumidity();
   dhtTemp = HT.readTemperature();
   currentMillis = millis();
   currentsecs = currentMillis / 1000;
   if ((unsigned long)(currentsecs - previoussecs) >= interval) {
    message = String(humidity) + "," + String(dhtTemp);
    sendMessage(message);
   }


  // parse for a packet, and call onReceive with the result:
  onReceive(LoRa.parsePacket());
}

void sendMessage(String outgoing) {
  LoRa.beginPacket();                   // start packet
  LoRa.write(MasterNode);              // add destination address
  LoRa.write(Node1);             // add sender address
  LoRa.write(msgCount);                 // add message ID
  LoRa.write(outgoing.length());        // add payload length
  LoRa.print(outgoing);                 // add payload
  LoRa.endPacket();                     // finish packet and send it
  msgCount++;                           // increment message ID
}

void onReceive(int packetSize) {
  if (packetSize == 0) return;          // if there's no packet, return

  // read packet header bytes:
  int recipient = LoRa.read();          // recipient address
  byte sender = LoRa.read();            // sender address
  byte incomingMsgId = LoRa.read();     // incoming msg ID
  byte incomingLength = LoRa.read();    // incoming msg length

  String incoming = "";

  while (LoRa.available()) {
    incoming += (char)LoRa.read();
  }
  
  Serial.print(incoming);

  if (incomingLength != incoming.length()) {   // check length for error
   // Serial.println("error: message length does not match length");
   ;
    return;                             // skip rest of function
  }

  // if the recipient isn't this device or broadcast,
  if (recipient != Node1 && recipient != 0xAA) {
    //Serial.println("This message is not for me.");
    ;
    return;                             // skip rest of function
  }
    Serial.println(incoming);
    incoming = String(incoming);
    if (incoming.equals("On")){
      digitalWrite(LED,HIGH);
    }
    if(incoming.equals("Off")){
      digitalWrite(LED,LOW);
    }
}
