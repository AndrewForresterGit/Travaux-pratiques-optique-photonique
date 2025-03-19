import serial
import numpy as np
import time
from collections import deque

# Configuration du port série
PORT = '/dev/cu.usbmodem14101'  # À adapter selon ton système (ex: "/dev/ttyUSB0" sur Linux)
BAUDRATE = 115200  # Augmente la vitesse de transmission si possible
DURATION = 5  # Durée d'enregistrement en secondes

# Utilisation d'un buffer performant
buffer_size = 10000  # Capacité maximale du buffer (ajuste selon tes besoins)
data_buffer = deque(maxlen=buffer_size)

start_time = time.time()

with serial.Serial(PORT, BAUDRATE, timeout=0) as ser:  # timeout=0 = lecture non bloquante
    print(f"Enregistrement des données sur {PORT} pendant {DURATION} secondes...")

    while time.time() - start_time < DURATION:
        line = ser.readline().decode("utf-8").strip()  # Lecture rapide sans bloquer
        if line:
            data_buffer.append(float(line))  # Ajout rapide au buffer

# Conversion en array NumPy et sauvegarde
data_array = np.array(data_buffer)
np.save("serial_data.npy", data_array)
print(f"Données enregistrées dans 'serial_data.npy' ({len(data_array)} valeurs).")
