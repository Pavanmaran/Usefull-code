// Date: 19 aug 2022
// Pawan Meena
// Copy right @2009

#include <SoftwareSerial.h>
SoftwareSerial mySerial(7, 8); // RX, TX
String msg;
void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  Serial.println("Goodnight moon!");
  pinMode(13, OUTPUT);
  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  //mySerial.println("Hello, world?");
  mySerial.print("AT+CMGF=1\r");
  mySerial.println("AT+CNMI=2,2,0,0,0\r"); // Eeceiving Mode Enabled
}

void loop() { // run over and over
  while (mySerial.available()) {
    char var = mySerial.read();
    msg += var;
    var = "";
  }

  Serial.println(msg);
  //Serial.println(msg.indexOf("Hi"));
  if(msg.indexOf("ON")!=-1){
    digitalWrite(13,HIGH);
  }
    else if(msg.indexOf("OFF")!=-1){
     digitalWrite(13,LOW);
    }
    else{
      Serial.println("Galat cammand");
    }
  delay(1000);
    msg = "";
}
