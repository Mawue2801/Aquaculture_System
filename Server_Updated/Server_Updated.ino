/*
  LoRa Simple Arduino Server :
  Support Devices: 
  * LoRa Mini
  * LoRa Shield + Arduino;
  * LoRa GPS Shield + Arduino. 
  
  Example sketch showing how to create a simple messageing server, 
  with the RH_RF95 class. RH_RF95 class does not provide for addressing or
  reliability, so you should only use RH_RF95 if you do not need the higher
  level messaging abilities.

  It is designed to work with the other example LoRa Simple Client

  modified 16 11 2016
  by Edwin Chen <support@dragino.com>
  Dragino Technology Co., Limited
*/
#include <SPI.h>
#include <RH_RF95.h>
#include <SoftwareSerial.h>
SoftwareSerial sim(10, 11);

// Singleton instance of the radio driver
RH_RF95 rf95;

int _timeout;
String _buffer;
String number = "+233544089527"; //-> change with your number

float frequency = 868.0;
String command;


void setup() 
{     
  Serial.begin(9600);
  _buffer.reserve(50);
  sim.begin(9600);
  delay(1000);
  while (!Serial) ; // Wait for serial port to be available
  //Serial.println("Start Sketch");
  if (!rf95.init())
    Serial.println("init failed");
  // Setup ISM frequency
  rf95.setFrequency(frequency);
  // Setup Power,dBm
  rf95.setTxPower(13);
  // Defaults BW Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
  //Serial.print("Listening on frequency: ");
  //Serial.println(frequency);
}

void loop()
{
  sendRequest("C1");
  waitForAnswer();
  sendRequest("C2");
  waitForAnswer();
  
 if(Serial.available() > 0) {
      command = Serial.read();
      if (command == "SendMessage")
      {
        sim.println("AT+CMGF=1");
        delay(200);
        sim.println("AT+CMGS=\"" + number + "\"\r");
        delay(200);
        String SMS = "Water Level Critically Low";
        sim.println(SMS);
        delay(100);
        sim.println((char)26);
        delay(200);
        _buffer = _readSerial();
      }
      else
      {
        sendRequest(command); 
      }   
 }
}

void waitForAnswer(){
  uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);
  if (rf95.waitAvailableTimeout(500))
  {
    if (rf95.recv(buf, &len))
    {
      String dataTotal = (char*)buf; 
      Serial.println(dataTotal);
    }
    
  }
}

void sendRequest(String request)
{
  String dataTotal = request;
  int dataLength = dataTotal.length();dataLength++;
  uint8_t total[dataLength];
  dataTotal.toCharArray(total,dataLength);
  rf95.send(total,dataLength);
  rf95.waitPacketSent();
}

String _readSerial() {
  _timeout = 0;
  while  (!sim.available() && _timeout < 12000  )
  {
    delay(13);
    _timeout++;
  }
  if (sim.available()) {
    return sim.readString();
  }
}
