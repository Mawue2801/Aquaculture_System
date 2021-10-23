/*
  LoRa Simple Client for Arduino :
  Support Devices: LoRa Shield + Arduino 
  
  Example sketch showing how to create a simple messageing client, 
  with the RH_RF95 class. RH_RF95 class does not provide for addressing or
  reliability, so you should only use RH_RF95 if you do not need the higher
  level messaging abilities.

  It is designed to work with the other example LoRa Simple Server
  User need to use the modified RadioHead library from:
  https://github.com/dragino/RadioHead

  modified 16 11 2016
  by Edwin Chen <support@dragino.com>
  Dragino Technology Co., Limited
*/

#include <SPI.h>
#include <RH_RF95.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 3

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

// Singleton instance of the radio driver
RH_RF95 rf95;

float frequency = 868.0;
float temperature = 0;

float calibration_value = 21.34 - 0.7;
int phval = 0; 
unsigned long int avgval; 
int buffer_arr[10],temp;
 
float ph_act;

void setup() 
{
  Serial.begin(9600);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  sensors.begin();
  //while (!Serial) ; // Wait for serial port to be available
  Serial.println("Start LoRa Client");
  if (!rf95.init())
    Serial.println("init failed");
  // Setup ISM frequency
  rf95.setFrequency(frequency);
  // Setup Power,dBm
  rf95.setTxPower(13);

  // Setup Spreading Factor (6 ~ 12)
  rf95.setSpreadingFactor(7);
  
  // Setup BandWidth, option: 7800,10400,15600,20800,31200,41700,62500,125000,250000,500000
  //Lower BandWidth for longer distance.
  rf95.setSignalBandwidth(125000);
  
  // Setup Coding Rate:5(4/5),6(4/6),7(4/7),8(4/8) 
  rf95.setCodingRate4(5);
}

void loop()
{
  uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);

  if (rf95.waitAvailableTimeout(3000))
  { 
    // Should be a reply message for us now   
    if (rf95.recv(buf, &len))
   {
      int dataLength;
      String Request = (char*)buf;
      Serial.println(Request);
      if (Request == "C1")
      {
        sensors.requestTemperatures(); 
        temperature=sensors.getTempCByIndex(0);
      
        for(int i=0;i<10;i++) 
         { 
         buffer_arr[i]=analogRead(A0);
         delay(30);
         }
         for(int i=0;i<9;i++)
         {
         for(int j=i+1;j<10;j++)
         {
         if(buffer_arr[i]>buffer_arr[j])
         {
         temp=buffer_arr[i];
         buffer_arr[i]=buffer_arr[j];
         buffer_arr[j]=temp;
         }
         }
         }
         avgval=0;
         for(int i=2;i<8;i++)
         avgval+=buffer_arr[i];
         float volt=(float)avgval*5.0/1024/6; 
         ph_act = -5.70 * volt + calibration_value;
        String data = "1-" + String(temperature) + "," + String(ph_act);
        int dataLength = data.length();dataLength++;
        uint8_t total[dataLength];
        data.toCharArray(total,dataLength);
        Serial.println(data);
        rf95.send(total,dataLength);
        rf95.waitPacketSent();
      }
     else if(Request.indexOf("A1") >= 0)
     {
      digitalWrite(5,HIGH);
      delay(500);
      digitalWrite(5,LOW);
      Serial.println("A1 Request Received");
     }
    }
  }
  delay(400);
}
