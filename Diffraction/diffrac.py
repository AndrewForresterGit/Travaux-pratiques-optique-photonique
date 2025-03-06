import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def analyze_diffraction_with_threshold(
    x_pixels,
    intensity,
    pixel_to_m,
    wavelength,
    L,
    n_minima=3,
    intensity_threshold=0.7,
    distance_points=5,
    prominence_val=0.02,
    filename = "res"
):
    """
    Calcule la largeur de la fente à partir du patron de diffraction.

    x_pixels : positions en pixels.
    intensity : intensités mesurées.
    pixel_to_m : conversion pixels -> mètres.
    wavelength : longueur d'onde (m).
    L : distance fente-écran (m).
    n_minima : nombre de minima par côté.
    intensity_threshold : seuil d'intensité.
    distance_points : distance minimale entre minima.
    prominence_val : prominence minimale.

    Return:
    slit_width_estimate : largeur estimée (m) ou None.
    x_m_centered : positions centrées sur le maximum.
    intensity_norm : intensité normalisée.
    """

    # Trouver indice maximum central
    index_max = np.argmax(intensity)
    
    # Conversion en mètres
    x_m = x_pixels * pixel_to_m
    
    # Normalisation intensité
    intensity_norm = intensity / np.max(intensity)
    
    # Récupérer le maximum central
    x_max_m = x_m[index_max]
    
    # Centrer sur le maximum central
    x_m_centered = x_m - x_max_m
    
    # Détection initiale des minima
    minima_indices, properties = find_peaks(
        -intensity_norm,
        distance=distance_points,
        prominence=prominence_val
    )
    
    # Filtrage par intensité : garde juste les minima < intensity_threshold
    minima_indices_filtered = [
        idx for idx in minima_indices
        if intensity_norm[idx] < intensity_threshold
    ]
    
    minima_indices_filtered = np.array(minima_indices_filtered)
    
    # Séparer minima gauche/droite par rapport au maximum
    left_mask = x_m_centered[minima_indices_filtered] < 0
    right_mask = x_m_centered[minima_indices_filtered] > 0
    
    left_minima_indices = minima_indices_filtered[left_mask]
    right_minima_indices = minima_indices_filtered[right_mask]
    
    # Trier par distance au centre
    left_minima_indices = left_minima_indices[np.argsort(np.abs(x_m_centered[left_minima_indices]))]
    right_minima_indices = right_minima_indices[np.argsort(np.abs(x_m_centered[right_minima_indices]))]
    
    # Considérer n minimas à gauche et à droite pour calculer
    left_minima_indices = left_minima_indices[:n_minima]
    right_minima_indices = right_minima_indices[:n_minima]
    
    # Calcul de largeur
    slit_widths = []
    nb_pairs = min(len(left_minima_indices), len(right_minima_indices))
    for i in range(nb_pairs):
        m = i + 1  # L'ordre du minimum
        x_left = np.abs(x_m_centered[left_minima_indices[i]])
        x_right = np.abs(x_m_centered[right_minima_indices[i]])
        y_avg = (x_left + x_right) / 2.0
        # Formule: a = m * lambda * L / y_avg
        a_estimate = m * wavelength * L / y_avg
        slit_widths.append(a_estimate)
    
    # Moyenne de lageur
    slit_width_estimate = np.mean(slit_widths)
    print(f"Largeur calculé : {slit_width_estimate:.3e} m")

    # Plot
    plt.figure(figsize=(8, 5))
    plt.scatter(x_m_centered, intensity_norm, s=1, label='Intensité normalisée')
    plt.xlabel("Position [m]")
    plt.ylabel("Intensité relative [-]")
    
    # Minima  (après filtrage)
    plt.plot(x_m_centered[minima_indices_filtered], intensity_norm[minima_indices_filtered],
             'rs', markersize=4, label='Minima identifié')
    
    # Annoter la largeur estimée
    if slit_width_estimate is None:
        plt.text(0.05, 0.95,
                 f"Largeur fente ≈ {slit_width_estimate:.3e} m",
                 transform=plt.gca().transAxes,
                 fontsize=12, verticalalignment='top',
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.grid(False)
    plt.margins(0)
    plt.legend()
    plt.savefig(filename, dpi=600, bbox_inches='tight')
    plt.show()
    
    return slit_width_estimate, x_m_centered, intensity_norm