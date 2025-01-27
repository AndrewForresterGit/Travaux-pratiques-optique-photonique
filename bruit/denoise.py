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
            
    return np.array(t), np.array(sig1), np.array(sig2)

def increasing_sampling(sig, sampling_range):
    samples = [i for i in range(*sampling_range)]
    standard_deviations = []
    for i in samples:
        sample_sig = sig[0:i]
        standard_deviations.append(np.std(sample_sig))

    return np.array(samples), np.array(standard_deviations)

data_path = 'donnees/scope_total.csv'

t, sync, sig = get_csv_data(data_path)
t = np.arange(0, len(sig), 1)


sig_high = np.where(sig > np.mean(sig), sig, 0)
sig_high = np.delete(sig_high, np.argwhere(sig_high==0))

sig_low = np.where(sig < np.mean(sig), sig, 0)
sig_low = np.delete(sig_low, np.argwhere(sig_low==0))

samples, standard_deviations_high = increasing_sampling(sig_high, (10, 5000, 10))
samples, standard_deviations_low = increasing_sampling(sig_low, (10, 5000, 10))


ax0 = plt.subplot(331)
ax0.hist(sig_high)
ax0.set_xlim(3.2, 3.35)
ax0.set_xlabel('Signal [V]')
ax0.set_ylabel('Nombre de mesure []')

ax1 = plt.subplot(333)
ax1.set_xlim(-0.05, 0.05)
ax1.hist(sig_low)
ax1.set_xlabel('Signal [V]')
ax1.set_ylabel('Nombre de mesure []')

ax2 = plt.subplot(312)

ax2.scatter(samples, standard_deviations_high, s=1)
ax2.set_xlabel('Nombre de mesure []')
ax2.set_ylabel('Moyenne [V]')

ax3 = plt.subplot(313)
ax3.scatter(samples, standard_deviations_low, s=1)
ax3.set_xlabel('Nombre de mesure []')
ax3.set_ylabel('Moyenne [V]')

plt.show()
