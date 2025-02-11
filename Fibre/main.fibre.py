import numpy as np
import matplotlib.pyplot as plt
from getcsvData import getcsvData_dict as getcsv

class fibre:
    def __init__(self, type, path):
        self.path = path
        self.type = type
        data = getcsv(path)
        keys = list(data.keys())
        self.position_raw = data[keys[0]]  # Récupère la colonne position
        self.intensité = data[keys[1]] # Récupère la colone intensité
        return
    def plot(self):
        plt.plot(self.position, self.intensité)
        return


# Les monomodes
mono_s = fibre("mono", "Fibre\Data\Mono_square_1.csv")
mono_x = fibre("mono", "Fibre\Data\Mono_x_1.csv")
mono_y = fibre("mono", "Fibre\Data\Mono_y_1.csv")

# Moyennement multimodes
moyen_s = fibre("moyen", "Fibre\Data\Moyen_square_1.csv")
moyen_x = fibre("moyen","Fibre\Data\Moyen_x_1.csv")
moyen_y = fibre("moyen","Fibre\Data\Moyen_y_1.csv")

# Hautement multimodes
haut_s = fibre("haut","Fibre\Data\Multi_square_1.csv")
haut_x = fibre("haut","Fibre\Data\Multi_x_1.csv")
haut_y = fibre("haut","Fibre\Data\Multi_y_1.csv")

mono_x.plot()
haut_x.plot()
plt.show()

