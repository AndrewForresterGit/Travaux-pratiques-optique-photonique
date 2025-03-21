import serial
import time
import numpy as np
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/cu.usbmodem14101', 250000, timeout=100)

print("start")
iterations = 10000
i = 0
arr = np.zeros(iterations)
temps = np.zeros(iterations)
start = time.time()
while i<iterations:
    arr[i] = float(ser.readline())#.decode('utf-8').strip())
    i += 1
delta = time.time() - start

print("done")
print(delta)
temps=np.linspace(0, delta, iterations)

np.save('tension_baud_test_38400.npy', arr)
np.save('temps_baud_test_38400.npy', temps)
plt.plot(temps, arr)
plt.scatter(temps, arr, s=2)
##plt.savefig(test.pdf)
plt.show()

ser.close()
