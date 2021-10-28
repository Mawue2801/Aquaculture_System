int temp;
int var = 0;
String text;
String command;
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
  if (command.indexOf("1-A1") >= 0)
  {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else if (command.indexOf("1-A0") >= 0)
  {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
delay(2000);
}
