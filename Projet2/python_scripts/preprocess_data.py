"""
Author: Andrew Forrester
Created: 2025-04-18
Description: ...
"""

import os
import wave
from glob import glob
import scipy.io
import numpy as np
import matplotlib.pyplot as plt


def extract(file: str) -> np.array:
    """read .mat or .npy"""
    filetype = file.split('.')[-1]
    
    if filetype == "mat": 
        raw_data = scipy.io.loadmat(file)['moku'][0][0][1]
    elif filetype == "npy":
        raw_data = np.load(file)
    else:
        raise ValueError("The file must be of type .mat or .npy")

    return raw_data

def reshape(data):
    time = [i[0] for i in data]
    signal = [i[1] for i in data]

    return np.array([time, signal])

def make_wave(data):
    return (data[1].T * (2**15 - 1)).astype("<h")

def preprocess(file: str, save_file: str):
    """
    files must have .mat or .npy extension
    saves file as a .npy and .wav
    save_file string must not have an extension
    """
    
    raw_data = extract(file)
    data = reshape(raw_data)
    audio = make_wave(data)

    # save npy
    np.save(save_file + ".npy", data)

    # save wav
    with wave.open(save_file + ".wav", "w") as f:
        f.setnchannels(1)
        # 2 bytes per sample.
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(audio.tobytes())

    return None

    
def main() -> None:
    """preprocesses the relevant data for the project 2 analysis"""

    # move into data the directory
    print(f"ran from {os.getcwd()}")
    os.chdir("../donnees")
    print(f"changed dir to {os.getcwd()}")

    # include sampling rates ...

    # petit plexiglass (1)
    sweep1 = "non_classe/sweep_with_smoll.mat"
    sweep1_save = "preprocessed/petit_plexi/sweep1"

    # moyen plexiglass (2)
    sweep2 = "non_classe/sweep.mat"
    sweep2_save = "preprocessed/moyen_plexi/sweep2"
    
    noise2 = "raw_mokugo/noise_30s.mat"
    noise2_save = "preprocessed/moyen_plexi/noise2"

    # grosse vitre (3)
    sweep3 = "raw_mokugo/freq_sweep_100-10k-30s.npy"
    sweep3_save = "preprocessed/grosse_vitre/sweep3"
    
    noise3 = "non_classe/dark_2.mat"
    noise3_save = "preprocessed/grosse_vitre/noise3"
    
    tests = [(sweep1, sweep1_save),
             (sweep2, sweep2_save), (noise2, noise2_save),
             (sweep3, sweep3_save), (noise3, noise3_save)]

    for i in tests:
        preprocess(*i)

if __name__ == "__main__":
    main()
