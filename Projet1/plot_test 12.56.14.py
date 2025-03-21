import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    temps = np.load('temps_baud_test_300.npy')
##    position_x = np.load('position_x.npy')
    tension = np.load('tension_baud_test_300.npy')
    plt.plot(temps, tension)

    
    plt.show()
