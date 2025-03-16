#include <SoftwareSerial.h>

#define BAUD_RATE 74880  // Configurable baud rate

// Setup SoftwareSerial for communication with Arduino B
// Here, pin 10 is RX and pin 11 is TX on Arduino A.
SoftwareSerial arduinoBSerial(10, 11);

void setup() {
  // Initialize hardware serial for communication with PC
  Serial.begin(BAUD_RATE);
  // Initialize SoftwareSerial for communication with Arduino B
  arduinoBSerial.begin(BAUD_RATE);

  Serial.println("Arduino A started. Waiting for data from PC...");
}

void loop() {
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
