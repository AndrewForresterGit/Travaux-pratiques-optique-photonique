"""
Author: Andrew Forrester
Created: 2025-04-18
Description: ...
"""

import os
import wave
from glob import glob
import numpy as np
import matplotlib.pyplot as plt


def preprocess(raw_data: list[tuple]) -> np.array:
    """changes list of tuples to a ndarray"""
    time = [i[0] for i in raw_data]
    signal = [i[1] for i in raw_data]

    return np.array([time, signal])


def main() -> None:
    """preprocesses the manual frequency sweep data"""

    # move into data directory
    print(f"ran from {os.getcwd()}")
    os.chdir("../donnees")
    print(f"changed dir to {os.getcwd()}")

    subdir = "raw_mokugo/manual_freq_sweep"
    sample_rate = 40e3

##    files = glob(f"{subdir}/*.npy")
    files = ["raw_mokugo/freq_sweep_100-10k-30s.npy"]

    for file in files:
        save_file = file.replace("raw_mokugo", "preprocessed")
        save_file_wave = save_file.replace("npy", "wav")
        raw_data = np.load(file)

        preprocessed_data = preprocess(raw_data)
##        np.save(save_file, preprocessed_data)

        audio = preprocessed_data[1].T
        audio = (audio * (2 ** 15 - 1)).astype("<h")

        with wave.open(save_file_wave, "w") as f:
            f.setnchannels(1)
            # 2 bytes per sample.
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            f.writeframes(audio.tobytes())

if __name__ == "__main__":
    main()
