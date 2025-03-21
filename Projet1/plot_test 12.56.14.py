import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    temps = np.load('temps_image.npy')
##    position_x = np.load('position_x.npy')
    tension = np.load('tension_image.npy')
    plt.plot(temps, tension)

    
    plt.show()
