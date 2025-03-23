#include <SoftwareSerial.h>

#define BAUD_RATE 9600   // Configurable baud rate

// Setup SoftwareSerial for communication with Arduino B
// Here, pin 10 is RX and pin 11 is TX on Arduino A.
// C'EST 11 LA PIN POUR TRANSMETTRE
SoftwareSerial arduinoBSerial(10, 11);

void setup() {
  // Initialize hardware serial for communication with PC
  Serial.begin(BAUD_RATE);
  // Initialize SoftwareSerial for communication with Arduino B
  arduinoBSerial.begin(BAUD_RATE);

  Serial.println("Arduino A started. Waiting for data from PC...");
}

void loop() {
    arduinoBSerial.print("72*73*105*120*118*125*116*95*70\n0*114*2*105*62*114*60*117*60\n88*7*29*124*155*144*122*138*60\n94*103*143*164*181*179*148*71*45\n109*159*141*202*256*202*141*159*109\n45*71*148*179*181*164*143*103*94\n60*138*122*144*155*124*29*7*88\n60*117*60*114*62*105*2*114*0\n70*95*116*125*118*120*105*73*72\n");
    
    //arduinoBSerial.print("a");
    //delay(100);
    //arduinoBSerial.print("*");
    //delay(100);
    //arduinoBSerial.print("Hello world!");
    delay(1000);

  // If data comes in from the PC, forward it to Arduino B.
  if (Serial.available()) {
    String dataFromPC = Serial.readStringUntil('\n');
    // Forward the data to Arduino B
    arduinoBSerial.println(dataFromPC);
  }
  
  // If data is received from Arduino B, send it back to the PC.
  if (arduinoBSerial.available()) {
    String dataFromB = arduinoBSerial.readStringUntil('\n');
    Serial.println(dataFromB);
  }
}
