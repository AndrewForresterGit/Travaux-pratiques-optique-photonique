import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt


t = np.linspace(0, 1, 1000, endpoint=False)
sig = 0.5*signal.square(4 * np.pi * t)+0.5
noise = np.random.normal(0,0.4,1000)

b, a = signal.butter(1, 20, 'lp', fs=1000, output='ba')
w, h = signal.freqs(b, a)
filtered = signal.filtfilt(b, a, sig+noise)

fig, (ax0, ax1, ax2) = plt.subplots(3, 1, layout='constrained')
ax0.plot(t, sig+noise)
ax0.set_xlabel('Time (s)')
ax0.set_ylabel('Signal')

ax1.set_xlabel('Frequency [rad/s]')
ax1.set_ylabel('Amplitude [dB]')
ax1.margins(0, 0.1)
ax1.grid(which='both', axis='both')
ax1.semilogx(w, 20 * np.log10(abs(h)))

ax2.plot(t, filtered)

plt.show()
