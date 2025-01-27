import csv
import numpy as np
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

def increasing_sampling(sig, sampling_range):
    samples = [i for i in range(*sampling_range)]
    averages = []
    for i in samples:
        sample_sig = sig[0:i]
        averages.append(sum(sample_sig)/len(sample_sig))

    return samples, averages

data_path = 'donnees/scope_total.csv'

t, sync, sig = get_csv_data(data_path)
sync = np.array(sync)
sig = np.array(sig)

sig_haut = np.trim_zeros(np.sort(
    np.where(sig > (max(sig)+min(sig))/2, sig, 0)))

sig_bas = np.trim_zeros(np.sort(
    np.where(sig < (max(sig)+min(sig))/2, sig, 0)))

samples, averages_haut = increasing_sampling(sig_haut, (1, 5000, 100))
samples, averages_bas = increasing_sampling(sig_bas, (1, 5000, 100))

##fig, (ax0, ax1, ax2, ax3) = plt.subplots(3, 1, layout='constrained')

ax0 = plt.subplot(331)
ax0.hist(sig_haut)
ax0.set_xlim(3.2, 3.35)
ax0.set_xlabel('Signal [V]')
ax0.set_ylabel('Nombre de mesure []')

ax1 = plt.subplot(333)
ax1.set_xlim(-0.05, 0.05)
ax1.hist(sig_bas)
ax1.set_xlabel('Signal [V]')
ax1.set_ylabel('Nombre de mesure []')

ax2 = plt.subplot(312)
ax2.scatter(samples, averages_haut)
ax2.set_xlabel('Nombre de mesure []')
ax2.set_ylabel('Moyenne [V]')

ax3 = plt.subplot(313)
ax3.scatter(samples, averages_bas)
ax3.set_xlabel('Nombre de mesure []')
ax3.set_ylabel('Moyenne [V]')

plt.show()
