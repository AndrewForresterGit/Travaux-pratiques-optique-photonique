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

    plt.plot(xf, 2.0/length * np.abs(yf[0:length//2]))
    plt.show()
    
def main() -> None:

    # move into data directory
    print(f"ran from {os.getcwd()}")
    os.chdir("../donnees")
    print(f"changed dir to {os.getcwd()}")

    subdir = "preprocessed/manual_freq_sweep"
    sample_rate = 40e3

    files = glob(f"{subdir}/*.wav")
    for file in files:
        title = file.split('_')[-1].split('.')[0]
        freq = float(title)
        print(freq)
    
        a = read(file)
        audio = np.array(a[1], dtype=float)
        fourier(audio, sample_rate)


##        fig = plt.figure()
##       
##        ax1 = fig.add_subplot(211)
##        ax1.set_title(title)
##        ax1.specgram(audio, NFFT=1024, Fs=sample_rate)
##
##        ax2 = fig.add_subplot(212)
##        ax2.magnitude_spectrum(audio, Fs=sample_rate, scale='dB', color='C1')
##        plt.show()
    
if __name__ == "__main__":
    main()

