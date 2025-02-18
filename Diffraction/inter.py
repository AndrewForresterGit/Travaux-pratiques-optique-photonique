#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from getcsvData import getcsvData_dict

def analyze_interference(intensity, conversion_factor, L, wavelength, prominence=0.05, plot_save=None):
    """
    Analyzes a 1D interference intensity profile and calculates the slit separation.

    Parameters:
        intensity (np.ndarray): 1D intensity array from Fiji.
        conversion_factor (float): Meters per pixel.
        L (float): Distance from slits to screen (in meters).
        wavelength (float): Wavelength of the light in nm.
        prominence (float): Prominence factor (fraction of max intensity) for peak detection.
        plot_save (str or None): If provided, the plot is saved to this path.

    Returns:
        slit_separation (float or None): Calculated slit separation in meters.
        avg_fringe_spacing (float or None): Average fringe spacing in meters.
    """
    # Create x-axis in physical units
    x_pixels = np.arange(len(intensity))
    x_physical = x_pixels * conversion_factor

    # Set peak prominence based on the maximum intensity
    peak_prominence = prominence * np.max(intensity)

    # Detect maxima and minima using find_peaks.
    peaks, _ = find_peaks(intensity, prominence=peak_prominence)
    valleys, _ = find_peaks(-intensity, prominence=peak_prominence)

    # Plot the intensity profile with detected points.
    plt.figure(figsize=(10, 6))
    plt.plot(x_physical, intensity, label="Intensity", color="blue")
    plt.scatter(x_physical[peaks], intensity[peaks], color="red", marker="o", label="Maxima")
    plt.scatter(x_physical[valleys], intensity[valleys], color="green", marker="x", label="Minima")
    plt.xlabel("Distance (m)")
    plt.ylabel("Intensity (a.u.)")
    plt.title("Double-Slit Interference Pattern")
    plt.legend()

    # Calculate the average fringe spacing and slit separation if enough peaks are detected.
    if len(peaks) < 2:
        print("Not enough maxima detected to calculate fringe spacing.")
        avg_fringe_spacing = None
        slit_separation = None
    else:
        fringe_spacings = np.diff(x_physical[peaks])
        avg_fringe_spacing = np.mean(fringe_spacings)
        print(f"Average fringe spacing: {avg_fringe_spacing:.4e} m")

        # Convert wavelength from nm to m.
        wavelength_m = wavelength * 1e-9

        # Using the formula: d = (λ L) / Δx, where Δx is the fringe spacing.
        slit_separation = (wavelength_m * L) / avg_fringe_spacing
        print(f"Calculated slit separation: {slit_separation:.4e} m")

        # Annotate the plot with the slit separation.
        plt.text(
            0.05, 0.95,
            f"Slit separation: {slit_separation:.2e} m",
            transform=plt.gca().transAxes,
            verticalalignment="top",
            bbox=dict(facecolor="white", alpha=0.6)
        )

    # Save the plot if a file path is provided.
    if plot_save:
        plt.savefig(plot_save)
        print(f"Plot saved to {plot_save}")

    plt.show()
    return slit_separation, avg_fringe_spacing

def main():
    # ----- Set Your Parameters Here -----
    input_file = "slice.npy"         # Path to your NumPy file containing a 1D intensity array.
    input =
    conversion_factor = 1e-6           # Conversion factor: meters per pixel.
    L = 1.0                          # Distance from slits to screen in meters.
    wavelength = 650                 # Wavelength in nm (use 650 or 632, etc.).
    prominence = 0.05                # Prominence factor for peak detection.
    plot_save = "interference_plot.png"  # File name to save the plot (or set to None).

    # ----- Load the intensity profile -----
##    try:
##        intensity = np.load(input_file)
##    except Exception as e:
##        print(f"Error loading file {input_file}: {e}")
    return

    if intensity.ndim != 1:
        print("Error: The input NumPy array must be a 1D intensity profile.")
        return

    # ----- Analyze the interference pattern -----
    analyze_interference(intensity, conversion_factor, L, wavelength, prominence, plot_save)

if __name__ == "__main__":
    main()
