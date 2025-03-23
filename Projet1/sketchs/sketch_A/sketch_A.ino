#include <AltSoftSerial.h>

#define BAUD_RATE 115200  // Change as needed
#define IMAGE_SIZE 1024   // 32x32 image: 1024 bytes

// AltSoftSerial on Arduino Uno uses fixed pins (RX: pin 8, TX: pin 9)
AltSoftSerial altSerial;

uint8_t imageBuffer[IMAGE_SIZE];

void setup() {
  Serial.begin(BAUD_RATE);     // For communication with the PC
  altSerial.begin(BAUD_RATE);   // For communication with Arduino B
  Serial.println("Arduino A: Ready");
}

void loop() {
  // Wait until data is available from the PC
  if (Serial.available()) {
    // Read the first line which should be the header
    String headerLine = Serial.readStringUntil('\n');
    headerLine.trim(); // Remove any whitespace/newline

    // Check what type of data we're receiving
    if (headerLine.startsWith("<TYPE:IMG>")) {
      // Image mode
      // Forward header to Arduino B
      altSerial.println(headerLine);
      Serial.println("Image mode initiated.");

      // Expect the <IMG_START> marker from the PC
      String marker = Serial.readStringUntil('\n');
      marker.trim();
      if (marker != "<IMG_START>") {
        Serial.println("Error: Expected <IMG_START>");
        return;
      }
      altSerial.println(marker);  // forward marker

      // Read IMAGE_SIZE bytes of binary image data
      int bytesRead = 0;
      while (bytesRead < IMAGE_SIZE) {
        if (Serial.available()) {
          int byteReceived = Serial.read();
          imageBuffer[bytesRead] = byteReceived;
          bytesRead++;
        }
      }
      // Forward the binary image data to Arduino B
      altSerial.write(imageBuffer, IMAGE_SIZE);

      // Expect the <IMG_END> marker from the PC
      String endMarker = Serial.readStringUntil('\n');
      endMarker.trim();
      if (endMarker != "<IMG_END>") {
        Serial.println("Error: Expected <IMG_END>");
        return;
      }
      altSerial.println(endMarker);  // forward end marker

      // Now, wait for the processed image response from Arduino B

      // Read response header from Arduino B
      while (!altSerial.available());
      String responseHeader = altSerial.readStringUntil('\n');
      responseHeader.trim();
      Serial.println(responseHeader);

      // Read the <IMG_START> marker
      while (!altSerial.available());
      String responseStart = altSerial.readStringUntil('\n');
      responseStart.trim();
      Serial.println(responseStart);

      // Read the processed image data (binary)
      int processedBytes = 0;
      while (processedBytes < IMAGE_SIZE) {
        if (altSerial.available()) {
          int byteReceived = altSerial.read();
          imageBuffer[processedBytes] = byteReceived;
          processedBytes++;
        }
      }
      // Send the processed image data back to the PC as binary
      Serial.write(imageBuffer, IMAGE_SIZE);

      // Read the <IMG_END> marker and forward it (optional)
      while (!altSerial.available());
      String responseEnd = altSerial.readStringUntil('\n');
      responseEnd.trim();
      Serial.println(responseEnd);
    }
    else if (headerLine.startsWith("<TYPE:TXT>")) {
      // Text mode
      altSerial.println(headerLine);
      Serial.println("Text mode initiated.");

      // Read the actual text message from the PC
      String textMessage = Serial.readStringUntil('\n');
      altSerial.println(textMessage);

      // Wait for the response from Arduino B and then send it back to the PC
      while (!altSerial.available());
      String response = altSerial.readStringUntil('\n');
      Serial.println(response);
    }
    else {
      Serial.println("Unknown header type received.");
    }
  }
}
