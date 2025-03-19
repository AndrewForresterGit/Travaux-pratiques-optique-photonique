import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    temps = np.load('temps.npy')
##    position_x = np.load('position_x.npy')
    tension = np.load('tension.npy')
    plt.plot(temps, tension)

    
    plt.show()
