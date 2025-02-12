import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from getcsvData import getcsvData_dict as getcsv


class fibre:
    def __init__(self, type_mode, path):
        self.path = path
        self.type_mode = type_mode
        data = getcsv(path)
        keys = list(data.keys())
        self.position_raw = np.array(data[keys[0]])
        self.position_norm = np.linspace(-62.5, 62.5, len(self.position_raw))
        self.intensité = np.array(data[keys[1]])

        # initialisaion de la figure
        self.fig = None
        self.ax = None
    
    def plot(self, xlabel, ylabel):
        self.fig = plt.figure()
        self.ax = self.fig.subplots()
        
        self.ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.xaxis.set_major_locator(tck.MultipleLocator(20))
        self.ax.yaxis.set_major_locator(tck.MultipleLocator(.1))
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.scatter(self.position_norm, self.intensité/603, label=self.type_mode, s=1, c='black')


# Les monomodes
mono_s = fibre("mono", "Data/Mono_square_1.csv")
mono_x = fibre("mono", "Data/Mono_x_1.csv")
mono_y = fibre("mono", "Data/Mono_y_1.csv")

# Moyennement multimodes
moyen_s = fibre("moyen", "Data/Moyen_square_1.csv")
moyen_x = fibre("moyen", "Data/Moyen_x_1.csv")
moyen_y = fibre("moyen","Data/Moyen_y_1.csv")

# Hautement multimodes
haut_s = fibre("haut","Data/Multi_square_1.csv")
haut_x = fibre("haut","Data/Multi_x_1.csv")
haut_y = fibre("haut","Data/Multi_y_1.csv")

mono_x.plot()
moyen_x.plot()
haut_x.plot(r"Position radiale [$\mu$m]", r"Intensité [%]", )

##plt.legend()
plt.show()

