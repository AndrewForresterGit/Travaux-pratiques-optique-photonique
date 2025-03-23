#include <AltSoftSerial.h>

#define BAUD_RATE 115200  // Must match Arduino A's setting
#define IMAGE_SIZE 1024   // 32x32 image: 1024 bytes

// AltSoftSerial on Arduino Uno uses fixed pins (RX: pin 8, TX: pin 9)
AltSoftSerial altSerial;

uint8_t imageBuffer[IMAGE_SIZE];

void setup() {
  altSerial.begin(BAUD_RATE);
}

void loop() {
  // Check if data is available from Arduino A
  if (altSerial.available()) {
    // Read the header line
    String headerLine = altSerial.readStringUntil('\n');
    headerLine.trim();

    if (headerLine.startsWith("<TYPE:IMG>")) {
      // Image mode
      // Read the <IMG_START> marker
      while (!altSerial.available());
      String marker = altSerial.readStringUntil('\n');
      marker.trim();
      if (marker != "<IMG_START>") {
        // Error handling can be added here if needed
      }
      
      // Read IMAGE_SIZE bytes of binary image data
      int bytesRead = 0;
      while (bytesRead < IMAGE_SIZE) {
        if (altSerial.available()) {
          int byteReceived = altSerial.read();
          imageBuffer[bytesRead] = byteReceived;
          bytesRead++;
        }
      }
      
      // Read the <IMG_END> marker
      while (!altSerial.available());
      String endMarker = altSerial.readStringUntil('\n');
      endMarker.trim();

      // Process the image (using a function that inverts grayscale values)
      processImage(imageBuffer, IMAGE_SIZE);

      // Now, send back the processed image with the same protocol
      altSerial.println(headerLine);  // Send header back
      altSerial.println("<IMG_START>");
      altSerial.write(imageBuffer, IMAGE_SIZE);
      altSerial.println("<IMG_END>");
    }
    else if (headerLine.startsWith("<TYPE:TXT>")) {
      // Text mode
      while (!altSerial.available());
      String textMessage = altSerial.readStringUntil('\n');

      // Process the text (for example, appending a message)
      String modifiedText = textMessage + " - Processed by Arduino B";
      altSerial.println(modifiedText);
    }
    else {
      // Unknown header: you might choose to ignore or handle this.
    }
  }
}

// A simple image processing function that inverts grayscale values.
// Replace this with your own processing function as needed.
void processImage(uint8_t* img, int len) {
  for (int i = 0; i < len; i++) {
    img[i] = 255 - img[i];
  }
}
