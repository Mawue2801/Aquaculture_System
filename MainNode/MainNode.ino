/*
  Master Lora Node
  https://www.electroniclinic.com/

*/
#include <SPI.h>              // include libraries
#include <LoRa.h>
 
byte MasterNode = 0xAA;     
byte Node1 = 0xBB;
byte Node2 = 0xCC; 

String SenderNode = "";
String outgoing;              // outgoing message

byte msgCount = 0;            // count of outgoing messages

// Tracks the time since last event fired
unsigned long previousMillis=0;
unsigned long int previoussecs = 0; 
unsigned long int currentsecs = 0; 
unsigned long currentMillis = 0;
int interval= 1 ; // updated every 1 second
int Secs = 0; 
String message = "";
char command;


void setup() {
  Serial.begin(9600);                   // initialize serial
  
  if (!LoRa.begin(915E6)) {             // initialize ratio at 915 MHz
    Serial.println("LoRa init failed. Check your connections.");
    while (true);                       // if failed, do nothing
  }

 Serial.println("LoRa init succeeded.");
}

void loop() {
currentMillis = millis();
   currentsecs = currentMillis / 1000;
   if ((unsigned long)(currentsecs - previoussecs) >= interval) {
    if (Serial.available() > 0){
        command = Serial.read();
        if (command == 'F'){
          message = "On";
          sendMessage(message,MasterNode, Node1);
        }
        if (command == 'S'){
          message = "On";
          sendMessage(message,MasterNode, Node2);
        }
        if (command == 'f'){
          message = "Off";
          sendMessage(message,MasterNode, Node1);
        }
        if (command == 's'){
          message = "Off";
          sendMessage(message,MasterNode, Node2);
        }
   }
    
   previoussecs = currentsecs;
    }

  // parse for a packet, and call onReceive with the result:
  onReceive(LoRa.parsePacket());
  delay(1000);
   
  }


void sendMessage(String outgoing, byte MasterNode, byte otherNode) {
  LoRa.beginPacket();                   // start packet
  LoRa.write(otherNode);              // add destination address
  LoRa.write(MasterNode);             // add sender address
  LoRa.write(msgCount);                 // add message ID
  LoRa.write(outgoing.length());        // add payload length
  LoRa.print(outgoing);                 // add payload
  LoRa.endPacket();                     // finish packet and send it
  msgCount++;                           // increment message ID
  Serial.println("Sent Message");
}

void onReceive(int packetSize) {
  if (packetSize == 0) return;          // if there's no packet, return

  // read packet header bytes:
  int recipient = LoRa.read();          // recipient address
  byte sender = LoRa.read();            // sender address
  if( sender == 0xBB )
  SenderNode = "Node1:";
  if( sender == 0xCC )
  SenderNode = "Node2:";
  byte incomingMsgId = LoRa.read();     // incoming msg ID
  byte incomingLength = LoRa.read();    // incoming msg length

  String incoming = "";

  while (LoRa.available()) {
    incoming += (char)LoRa.read();
  }

 // if (incomingLength != incoming.length()) {   // check length for error
    //Serial.println("error: message length does not match length");
   // ;
   // return;                             // skip rest of function
 // }

  // if the recipient isn't this device or broadcast,
 // if (recipient != Node1 && recipient != MasterNode) {
   // Serial.println("This message is not for me.");
    //;
   // return;                             // skip rest of function
//  }

  // if message is for this device, or broadcast, print details:
  //Serial.println("Received from: 0x" + String(sender, HEX));
  //Serial.println("Sent to: 0x" + String(recipient, HEX));
  //Serial.println("Message ID: " + String(incomingMsgId));
 // Serial.println("Message length: " + String(incomingLength));
 // Serial.println("Message: " + incoming);
  //Serial.println("RSSI: " + String(LoRa.packetRssi()));
 // Serial.println("Snr: " + String(LoRa.packetSnr()));
 // Serial.println();

 if( sender == 0xBB )
 { 
  Serial.print("From0XBB:");
  Serial.println(incoming);
 }

  if( sender == 0xCC )
 { 
  Serial.print("From0XCC:");
  Serial.println(incoming);
 }

}
