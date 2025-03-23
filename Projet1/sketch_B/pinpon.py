import serial
import time


# Input image
#image_file = "emoji_compressed.bin"

# Configure the serial port. Change 'COM3' to your Arduino's port.
ser = serial.Serial('COM7', 300, timeout=1000)

# Give the connection a moment to initialize
time.sleep(2)

# Prepare and send the header with image metadata.
#header = "<TYPE:IMG;SIZE:1024;DIM:32x32>\n"
#ser.write(header.encode('utf-8'))
#time.sleep(0.1)  # Short delay for synchronization

# Send the start marker for the image data.
#ser.write("<IMG_START>\n".encode('utf-8'))
#time.sleep(0.1)


while True:
    """penar
    # Read the image file and send its binary contents.
    with open(image_file, "rb") as f:
        image_data = f.read()
        if len(image_data) != 1024:
            print("Warning: The image file is not 1024 bytes.")
    ##    print(image_data)
    ##    ser.write(image_data)

    # Send the end marker to signal the end of image data."
    """
##ser.write("<IMG_END>\n".encode('utf-8'))
#    ser.write(input(send_b:).)
    ser.write(input("Send: ").encode('utf-8'))
    #ser.write(input("Send: "))#.encode('utf-8'))

    time.sleep(0.1)

    # Optionally, read back the processed image or any response from Arduino A.
  #  while ser.in_waiting:
  #      response = ser.readline().decode('utf-8').strip()
  #      print("Response:", response)
        

ser.close()