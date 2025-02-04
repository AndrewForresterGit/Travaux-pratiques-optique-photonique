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
##            sig1.append(0.001*(0.2*float(data[1])-60))
            sig1.append(float(data[1]))
            sig2.append(float(data[2]))
            
    return np.array(t), np.array(sig1), np.array(sig2)

def increasing_sampling(sig, sampling_range):
    samples = [i for i in range(*sampling_range)]
    standard_deviations = []
    averages = []
    for i in samples:
        sample_sig = sig[0:i]
        standard_deviations.append(np.std(sample_sig))
        averages.append(np.mean(sample_sig))

    return np.array(samples), np.array(standard_deviations), np.array(averages)

data_path = 'donnees/scope_total.csv'
data_path = "bruit\donnees\scope_total.csv"

t, sig, sync = get_csv_data(data_path)
t = np.arange(0, len(sig), 1)


sig_high = np.where(sync > np.mean(sync), sig, 0)
sig_high = np.delete(sig_high, np.argwhere(sig_high==0))

sig_low = np.where(sync < np.mean(sync), sig, 0)
sig_low = np.delete(sig_low, np.argwhere(sig_low==0))


samples, standard_deviations_high, averages_high = increasing_sampling(sig_high, (10, 5000, 10))
samples, standard_deviations_low, averages_low = increasing_sampling(sig_low, (10, 5000, 10))


ax0 = plt.subplot(221)
ax0.scatter(samples, averages_high, s=1)
ax0.set_title('Moyenne du mode expérience')
ax0.set_xlabel('Nombre de mesure [-]')
ax0.set_ylabel('Signal [V]')

ax1 = plt.subplot(222)
ax1.scatter(samples, averages_low, s=1)
ax1.set_title('Moyenne du mode lambda')
ax1.set_xlabel('Nombre de mesure [-]')
ax1.set_ylabel('Signal [V]')

ax2 = plt.subplot(223)
ax2.scatter(samples, standard_deviations_high, s=1)
ax2.set_title('Écart type du mode expérience')
ax2.set_xlabel('Nombre de mesure [-]')
ax2.set_ylabel('Écart type [V]')

ax3 = plt.subplot(224)
ax3.scatter(samples, standard_deviations_low, s=1)
ax3.set_title('Écart type du mode lambda')
ax3.set_xlabel('Nombre de mesure [-]')
ax3.set_ylabel('Écart type [V]')

print(np.mean(sig_high))
print(np.mean(sig_low))
      
plt.show()