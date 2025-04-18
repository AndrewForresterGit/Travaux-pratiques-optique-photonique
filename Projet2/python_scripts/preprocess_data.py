import os
from glob import glob
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

"""
Author: Andrew Forrester
Created: 2025-04-18
Description: ...
"""

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

    files = glob(f"{subdir}/*.npy")

    for file in files:
        save_file = file.replace("raw_mokugo", "preprocessed")
        raw_data = np.load(file)

        preprocessed_data = preprocess(raw_data)
        np.save(save_file, preprocessed_data)

if __name__ == "__main__":
    main()
