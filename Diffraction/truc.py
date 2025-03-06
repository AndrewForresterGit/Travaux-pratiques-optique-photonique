from diffrac import analyze_diffraction_with_threshold as swe
import numpy as np
from getcsvData import getcsvData_dict as getcsv

# Andrew
#file_path = "Diffraction\Cheveux\A_rouge15cm.csv" #Rouge
#file_path = "Diffraction\Cheveux\A_vert_10.csv" #Vert

# Mathieu
file_path = "Diffraction\Cheveux\M_rouge_15cm.csv" #Rouge
#file_path = "Diffraction\Cheveux\M_1_vert_15cm.csv" #Vert
#file_path = "Diffraction\Cheveux\M_1_vert_15_2cm.csv" #Vert


#file_path = "Diffraction\one_slit\R_0.04_15cm.csv"
#file_path = "Diffraction\one_slit\R_0.08_13cm.csv"
#file_path = "Diffraction\one_slit\V_0.04_1m_15cm.csv"
#file_path = "Diffraction\one_slit\V_0.08_0.5_15cm.csv"



dict = getcsv(file_path)

#print(dict.keys())

x = np.array(dict["Distance_(pixels)"])
I = np.array(dict["Gray_Value"])

#l_onde =  532e-9 #Vert
l_onde = 650e-9 #Rouge


penis = float(0.15/len(I))

chose = swe(x, I, penis, l_onde, 0.5, 5, filename="test")

#print(chose[0])
