import numpy as np
import matplotlib.ticker as tck
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from getcsvData import getcsvData_dict


def determine_maxima(scheme_dict, measure, screen_slit, longueur_onde):
    Distance_pixels, Gray_Value = scheme_dict.values()
    
    pos = np.array(Distance_pixels)
    pos_fixed = np.arange(-measure/2, measure/2, measure/len(pos))
    gray_scale = np.array(Gray_Value)
    
    # reperer les piques du schema
    peaks = find_peaks(gray_scale, threshold=0)[0]
    peaks_pos = np.zeros(len(peaks))
    peaks_int = np.zeros(len(peaks))
    
    for i, j in enumerate(peaks):
        peaks_pos[i] = pos_fixed[j]
        peaks_int[i] = gray_scale[j]

    # identifier visuellement le premier pique a partir du centre
##    fig_ident, ax_ident = plt.subplots()
##    ax_ident.scatter(pos_fixed, gray_scale, s=1)
##    ax_ident.scatter(peaks_pos, peaks_int)
##    plt.show()
    
    index = int(input('index du premier maximum: '))
    pos_peak_1 = peaks_pos[index]
    
    d = np.sqrt(pow(1/(pos_peak_1/screen_slit), 2) + 1)*longueur_onde
    print(f'distance d = {d:.3e} [m]')

    fig_display, ax_display = plt.subplots()
    
    ax_display.axvline(x=peaks_pos[index], color='red', linestyle=':', linewidth=1)
    ax_display.scatter(pos_fixed, gray_scale/gray_scale.max(), s=1)
##    xmin, xmax = ax_display.get_xlim()
##    ax_display.hlines(y=peaks_int[index]/gray_scale.max(), xmin=xmin, xmax=xmax, color='red', linestyle='-', linewidth=1)
    ax_display.scatter(peaks_pos[index], peaks_int[index]/gray_scale.max(), color='green', marker='s')

    # formatage du graphique
    ax_display.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax_display.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax_display.set_xlabel(r"Position sur l'écran [m]")
    ax_display.set_ylabel(r"Intensité relative [-]")
##    ax_display.margins(0)
##    plt.show()
    
    fig_display.savefig("figures_interference/R_50_10.pdf", format="pdf")


    return peaks_pos, peaks_int 

if __name__ == "__main__":
    '''
    ---longueurs d'ondes---
    laser vert: 535 [nm]
    laser rouge: 650 [nm]
    '''
    vert = 535e-9
    rouge = 650e-9
    
    fich_v_100_15 = '_two_SLIT/v_double_1m_15cm.csv'
    fich_v_75_15 = '_two_SLIT/V_0.75m_15cm.csv'
    fich_v_50_15 = '_two_SLIT/V_0.5_15cm.csv'
    fich_r_50_10 = '_two_SLIT/R_0.5_10cm.csv'

    data_V_100 = getcsvData_dict(fich_v_100_15) # indice=5, threshold=1
    data_V_75 = getcsvData_dict(fich_v_75_15) # indice=29, threshold=0
    data_V_50 = getcsvData_dict(fich_v_50_15) # indice=38, threshold=0
    data_R_50_10 = getcsvData_dict(fich_r_50_10) # indice=25, threshold=0
    
    peak_pos, peak_int = determine_maxima(data_R_50_10, .1, .50, longueur_onde=rouge)

##    plt.show()
