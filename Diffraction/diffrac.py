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
    prominence_val=0.01
):
    """
    Analyse le patron de diffraction et applique un seuil pour ignorer les minima non pertinents.
    
    Paramètres
    ----------
    x_pixels : np.array ou list
        Tableau des positions en pixels.
    intensity : np.array ou list
        Tableau des intensités mesurées.
    pixel_to_m : float
        Facteur de conversion des pixels en mètres.
    wavelength : float
        Longueur d'onde (en mètres).
    L : float
        Distance fente-écran (en mètres).
    n_minima : int
        Nombre de minima à détecter de chaque côté du maximum central.
    intensity_threshold : float
        Seuil maximum d'intensité pour qu'un point soit considéré comme un minimum réel (ex: 0.5).
    distance_points : int
        Distance minimale (en nombre de points) entre deux minima détectés.
    prominence_val : float
        Prominence minimale pour qu'un minimum soit conservé.
    
    Renvoie
    -------
    slit_width_estimate : float ou None
        Estimation de la largeur de la fente (en mètres), si possible.
    x_m_centered : np.array
        Positions (en mètres) centrées sur le maximum.
    intensity_norm : np.array
        Intensité normalisée.
    """
    # Conversion x_pixels en array NumPy si nécessaire
    x_pixels = np.array(x_pixels, dtype=float)
    intensity = np.array(intensity, dtype=float)
    
    # 1) Trouver l'indice du maximum central
    index_max = np.argmax(intensity)
    
    # 2) Conversion en mètres (sans recentrage)
    x_m = x_pixels * pixel_to_m
    
    # 3) Normalisation de l'intensité
    intensity_norm = intensity / np.max(intensity)
    
    # 4) Récupérer le maximum central (en mètres)
    x_max_m = x_m[index_max]
    
    # 5) Recentrer sur le maximum central
    x_m_centered = x_m - x_max_m
    
    # 6) Détection initiale des minima
    #    On cherche les "pics" de -intensity_norm
    #    distance=distance_points => écarte les minima trop proches
    #    prominence=prominence_val => ignore les minima trop peu profonds
    minima_indices, properties = find_peaks(
        -intensity_norm,
        distance=distance_points,
        prominence=prominence_val
    )
    
    # 7) Filtrage par intensité : on ne garde que les minima < intensity_threshold
    #    i.e. intensity_norm[minima] < 0.5 par exemple
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
    
    # Ne garder que n_minima de chaque côté
    left_minima_indices = left_minima_indices[:n_minima]
    right_minima_indices = right_minima_indices[:n_minima]
    
    # 8) Estimation de la largeur de la fente à partir du premier minimum
    if len(left_minima_indices) == 0 or len(right_minima_indices) == 0:
        print("Impossible d'estimer la largeur de la fente (pas assez de minima détectés).")
        slit_width_estimate = None
    else:
        # Premier minima (le plus proche du centre)
        x_left = np.abs(x_m_centered[left_minima_indices[0]])
        x_right = np.abs(x_m_centered[right_minima_indices[0]])
        y_min = (x_left + x_right) / 2.0
        
        # Relation a ~ λ * L / y_min (m=1, sin θ ~ θ ~ y/L)
        slit_width_estimate = wavelength * L / y_min
        print(f"Largeur de la fente estimée : {slit_width_estimate:.3e} m")
    
    # 9) Tracé
    plt.figure(figsize=(8, 5))
    plt.plot(x_m_centered, intensity_norm, label='Intensité normalisée')
    plt.xlabel("Position (m) [centrée sur le maximum]")
    plt.ylabel("Intensité relative")
    plt.title("Patron de diffraction (avec seuil sur les minima)")
    
    # Tracer tous les minima détectés (avant filtrage) en rouge
    # Pour montrer la différence, on peut faire un find_peaks(-intensity_norm) sans filtrage
    all_minima_indices, _ = find_peaks(-intensity_norm)
    plt.plot(x_m_centered[all_minima_indices], intensity_norm[all_minima_indices],
             'ro', label='Minima bruts')
    
    # Minima retenus (après filtrage)
    plt.plot(x_m_centered[minima_indices_filtered], intensity_norm[minima_indices_filtered],
             'go', label='Minima filtrés')
    
    # Marquage distinct pour ceux utilisés (les n_minima de chaque côté)
    if len(left_minima_indices) > 0:
        plt.plot(x_m_centered[left_minima_indices], intensity_norm[left_minima_indices],
                 'bs', markersize=8, label=f'{n_minima} minima (gauche)')
    if len(right_minima_indices) > 0:
        plt.plot(x_m_centered[right_minima_indices], intensity_norm[right_minima_indices],
                 'ms', markersize=8, label=f'{n_minima} minima (droite)')
    
    # Annoter la largeur estimée
    if slit_width_estimate is not None:
        plt.text(0.05, 0.95,
                 f"Largeur fente ≈ {slit_width_estimate:.3e} m",
                 transform=plt.gca().transAxes,
                 fontsize=12, verticalalignment='top',
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.grid(False)
    plt.legend()
    plt.show()
    
    return slit_width_estimate, x_m_centered, intensity_norm

# ----------------------------------------------------------------------
# Exemple d'utilisation (données simulées)
if __name__ == '__main__':
    # Génération de données fictives
    N = 1024
    x_pixels = np.linspace(0, N-1, N)
    pixel_to_m = 1e-6       # 1 pixel = 1 micron
    wavelength = 650e-9     # 650 nm
    L = 1.0                 # 1 m
    a_true = 50e-6          # largeur de la fente

    # Profil "sinc^2" + bruit
    x_centered_m = (x_pixels - N/2) * pixel_to_m
    beta = (np.pi * a_true / wavelength) * (x_centered_m / L)
    intensity_theo = (np.sinc(beta/np.pi))**2
    noise = np.random.normal(0, 0.03, size=intensity_theo.shape)
    intensity_noisy = intensity_theo + noise
    intensity_noisy[intensity_noisy < 0] = 0
    
    # Analyse avec seuil
    analyze_diffraction_with_threshold(
        x_pixels,
        intensity_noisy,
        pixel_to_m,
        wavelength,
        L,
        n_minima=3,
        intensity_threshold=0.5,   # ignorer les minima au-dessus de 0.5
        distance_points=15,       # minima espacés d'au moins 15 pixels
        prominence_val=0.02       # minima bien marqués
    )
