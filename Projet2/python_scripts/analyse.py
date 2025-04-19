"""
Author: Andrew Forrester
Created: 2025-04-18
Description: ...
"""

import os
import wave
from glob import glob
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from scipy.io.wavfile import read
import matplotlib.pyplot as plt


def fourier(audio, sample_rate):
    length = len(audio)
    yf = fft(audio)
    xf = fftfreq(length, 1/sample_rate)[:length//2]

    return xf, 2.0/length * np.abs(yf[0:length//2])
    
def main() -> None:

    # move into data directory
    print(f"ran from {os.getcwd()}")
    os.chdir("../donnees")
    print(f"changed dir to {os.getcwd()}")

##    subdir = "preprocessed/manual_freq_sweep"
    sample_rate = 40e3

    freqs = []
    amps = []

##    files = glob(f"{subdir}/*.wav")
    # dark
    file1 = 
    # vitre
    file2 = "preprocessed/freq_sweep_100-10k-30s.wav"
    # petit plexiglass
    file3 = "Plexigalss/small_plexi_100-10000_30s_sweep_with_smoll.wav"
    
    a = read(file1)
    audio = np.array(a[1], dtype=float)
    f, t, Sxx = signal.spectrogram(audio, fs=sample_rate)
    plt.specgram(audio, Fs=sample_rate)
    plt.show()


    fig = plt.figure()

    ax = fig.add_subplot()#projection='3d')
    X, Y = np.meshgrid(f, t, indexing='ij')
    amps = np.apply_along_axis(np.max, 1, Sxx)
##    print(amps.shape)

    plt.semilogx(f, 20*np.log(amps/np.max(amps)))

##    ax.plot_surface(X, Y, 20*np.log(Sxx), cmap='viridis')
##   
##    ax1 = fig.add_subplot(211)
##    ax1.set_title(title)
##    ax1.specgram(audio, NFFT=1024,s Fs=sample_rate)
##
##    ax2 = fig.add_subplot(212)
##    ax2.magnitude_spectrum(audio, Fs=sample_rate, scale='dB', color='C1')
    plt.show()

    
if __name__ == "__main__":
    main()

