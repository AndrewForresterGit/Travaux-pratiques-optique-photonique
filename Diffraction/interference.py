import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from getcsvData import getcsvData_dict


def analyse_interference(
    intensity,
    position_px,
    m_par_px,
    ):

    position_m = position_px *m_par_px
    plt.plot(position_m, intensity)
    plt.show()


if __name__ == '__main__':
    vert_single_1m = '_two_SLIT/v_double_1m_15cm.csv'
    data = getcsvData_dict(vert_single_1m)
    intensity = np.array(data['Gray_Value'])
    position = np.array(data['Distance_(pixels)'])

    analyse_interference(intensity, position, 1)
