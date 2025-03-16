#include <SoftwareSerial.h>

#define BAUD_RATE 74880  // Configurable baud rate

// Setup SoftwareSerial for communication with Arduino A
// Here, pin 10 is RX and pin 11 is TX on Arduino B.
SoftwareSerial arduinoASerial(10, 11);

void setup() {
  arduinoASerial.begin(BAUD_RATE);
}

void loop() {
  // Check if data is available from Arduino A
  if (arduinoASerial.available()) {
    String receivedData = arduinoASerial.readStringUntil('\n');
    
    // Process the data (for example, append a confirmation message)
    String modifiedData = receivedData + " - Modified by Arduino B";
    
    // Send the modified data back to Arduino A
    arduinoASerial.println(modifiedData);
  }
}
