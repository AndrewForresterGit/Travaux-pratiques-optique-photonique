import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from getcsvData import getcsvData_dict as getcsv


class fibre:
    def __init__(self, type_mode, path, a):
        self.path = path
        self.type_mode = type_mode
        data = getcsv(path)
        keys = list(data.keys())
        self.position_raw = np.array(data[keys[0]])
        self.position_norm = np.linspace(-a, a, len(self.position_raw))
        self.intensité = np.array(data[keys[1]])
        self.a = a

        # initialisaion de la figure
        self.fig = None
        self.ax = None
    
    def plot(self, xlabel, ylabel):
        self.fig = plt.figure()
        self.ax = self.fig.subplots()
        
        self.ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.xaxis.set_major_locator(tck.MultipleLocator(int(self.a/3)))
        self.ax.yaxis.set_major_locator(tck.MultipleLocator(.1))
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.scatter(self.position_norm, self.intensité/603, label=self.type_mode, s=1, c='black')


# Les monomodes
mono_s = fibre("mono", "Data/Mono_square_1.csv", a=3.6)
mono_x = fibre("mono", "Data/Mono_x_1.csv", a=3.6)
mono_y = fibre("mono", "Data/Mono_y_1.csv", a=3.6)

# Moyennement multimodes
moyen_s = fibre("moyen", "Data/Moyen_square_1.csv", a=25)
moyen_x = fibre("moyen", "Data/Moyen_x_1.csv", a=25)
moyen_y = fibre("moyen","Data/Moyen_y_1.csv", a=25)

# Hautement multimodes
haut_s = fibre("haut","Data/Multi_square_1.csv", a=62.5)
haut_x = fibre("haut","Data/Multi_x_1.csv", a=62.5)
haut_y = fibre("haut","Data/Multi_y_1.csv", a=62.5)

mono_x.plot(r"Position radiale [$\mu$m]", r"Intensité [%]")
moyen_x.plot(r"Position radiale [$\mu$m]", r"Intensité [%]")
haut_x.plot(r"Position radiale [$\mu$m]", r"Intensité [%]")

##plt.legend()
plt.show()

