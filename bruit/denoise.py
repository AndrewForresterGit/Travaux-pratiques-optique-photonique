import csv
import numpy as np
from scipy import signal
##from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt


def get_csv_data(filepath):
    t, sig1, sig2 = [], [], []
    with open(filepath) as f:
        csv_reader = csv.reader(f, delimiter=',')

        for i, data in enumerate(csv_reader):
            if i < 2: #skip header
                continue
            t.append(float(data[0]))
            sig1.append(0.2*float(data[1])-60)
            sig2.append(float(data[2]))
    return t, sig1, sig2

def weighted_average(sig1, sig2, state, samples):
    if state == 'haut':
        expression = lambda x: sig2[x] > (max(sig2)+min(sig2))/2
    else:
        expression = lambda x: sig2[x] < (max(sig2)+min(sig2))/2
    summed_sig = []
    for i, data in enumerate(sig1):
        if len(summed_sig) == samples:
            return sum(summed_sig)/len(summed_sig)
        if expression(i):
            summed_sig.append(data)
            
    print(len(summed_sig))
    return sum(summed_sig)/len(summed_sig)

def increasing_sampling(sig1, sig2):
    samples = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 5092]
    averages_haut = []
    averages_bas = []
    
    for i in samples:
        averages_haut.append(weighted_average(sig1, sig2, 'haut', i))
        averages_bas.append(weighted_average(sig1, sig2, 'bas', i))

    return samples, averages_haut, averages_bas

data_path = 'donnees/scope_total.csv'

t, sync, sig = get_csv_data(data_path)
t = np.arange(0, len(sig), 1)
samples, average_haut, average_bas = increasing_sampling(sig, sync)
print(samples, '\n', average_haut, '\n', average_bas)

plt.hist(samples, average_haut)

##fig, (ax0, ax1, ax2) = plt.subplots(3, 1, layout='constrained')

##b, a = signal.butter(1, 1000, 'lp', fs=10000, output='ba')
##w, h = signal.freqs(b, a)
##filtered = signal.filtfilt(b, a, sig)

##ax0.plot(t, sig)
##ax0.set_xlabel('Temps [s]')
##ax0.set_ylabel('Signal bruité [V]')
##
##ax1.plot(t, sync)
##ax1.set_xlabel('Temps [s]')
##ax1.set_ylabel('Signal\n synchronisation [V]')

##ax2.plot()

##ax2.plot(t, filtered)
##ax2.set_xlabel('Temps [s]')
##ax2.set_ylabel('Signal filtré')

##print('sans filtre:')
##print(f"haut: {weighted_average(sig, sync, 'haut', 10000):.4f} V")
##print(f"bas: {weighted_average(sig, sync, 'bas', 10000):.4f} V\n")
##print('avec filtre :')
##print(f"haut: {weighted_average(filtered, sync, 'haut'):.4f} V")
##print(f"bas: {weighted_average(filtered, sync, 'bas'):.4f} V")

plt.show()
