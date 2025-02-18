from diffrac import analyze_diffraction_with_threshold as swe
import numpy as np
from getcsvData import getcsvData_dict as getcsv


file_path = "Diffraction\Cheveux\M_1_vert_15_2cm.csv"
dict = getcsv(file_path)

print(dict.keys())

x = np.array(dict["Distance_(pixels)"])
I = np.array(dict["Gray_Value"])

l_onde =  532e-9
#l_onde = 650e-9


penis = float(0.15/len(I))

swe(x, I, penis, l_onde, 0.5, 6)