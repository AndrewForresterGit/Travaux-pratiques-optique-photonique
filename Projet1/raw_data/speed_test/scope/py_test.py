import time
import numpy as np
import matplotlib.pyplot as plt

# Nombre d'itérations
num_iterations = 100000

# Stocker les timestamps
timestamps = []

# Démarrer la boucleS
for _ in range(num_iterations):
    timestamps.append(time.time())

# Calculer les différences entre timestamps consécutifs
time_diffs = np.diff(timestamps)

# Temps total et statistiques
total_time = timestamps[-1] - timestamps[0]
mean_time = np.mean(time_diffs)
std_dev = np.std(time_diffs)

# Affichage des résultats
print(f"Temps total : {total_time:.6f} s")
print(f"Temps moyen par itération : {mean_time:.9f} s")
print(f"Écart-type : {std_dev:.9f} s")

# Histogramme avec échelle Y logarithmique
plt.hist(time_diffs, bins=50, edgecolor='black')
plt.yscale('log')
plt.xlabel("Temps entre itérations (s)")
plt.ylabel("Nombre d'occurrences (log)")
plt.title("Histogramme des durées entre itérations")
plt.show()
