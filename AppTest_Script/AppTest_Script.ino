int temp;
int var = 0;
String text;
int messageEnd;
int numberEnd;
String command;
String number;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
randomSeed(analogRead(5));
}

void loop() {
  // put your main code here, to run repeatedly:
temp = random(10);
text = "1-" + String(temp) + "," + String(var) + "," + String(var) + "," + String(var) + "," + String(var) + "," + String(var);
Serial.println(text);
if(Serial.available()>0)
{
  command = Serial.readString();
  if (command.indexOf("SMS") >= 0)
  {
    numberEnd = command.indexOf("-");
    messageEnd = command.indexOf("\r\n");
    Serial.println(command.substring(3,numberEnd));
    Serial.println(command.substring(numberEnd+1,messageEnd));
  }
  else if (command.indexOf("1-A0") >= 0)
  {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
delay(2000);
}
