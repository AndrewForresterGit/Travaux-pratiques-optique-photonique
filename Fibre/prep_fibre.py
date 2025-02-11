import numpy as np
import matplotlib.pyplot as plt

#cst
w0_laser = 0.315e-3  # Rayon du faisceau à la sortie du laser (m)
theta = 0.65e-3  # Demi-angle de divergence (rad)
lambda_laser = 632.8e-9  # Longueur d'onde du laser en (m)
f = 4.5e-3  # Focale de la lentille
NA = 0.12  
lambda_c = 620e-9   # Longueur d'onde de coupure (m)
V_c = 2.4048     # V pour fibre mono

#calculs de shit

# rayon de la fibre
a = (V_c * lambda_c) / (2*np.pi*(NA))
print(f'a = {a}')

# Calcul de V
V = 2*np.pi*a*NA/lambda_laser
print(f'V = {V}')

# Calcul du rayon du mode fondamentale de la fibre
w_0 = a*( 0.65 + 1.619*(V)**(-1.5) + 2.879*(V)**(-6) )
print(f'w_0 = {w_0}')


# Calcul de Z opti (en possant que w_0 = w_image)
w_image = w_0
w_obj = lambda_laser*f / (np.pi*w_image)
Z = np.sqrt( (w_obj / w0_laser)**2 - 1 ) * w0_laser / theta
print(f'Z_opti = {Z}')

# Calcul de T de selon z
Z_values = np.linspace(0, 1.6, 1000)  # Valeurs de Z en cm
w_2 = lambda_laser * f / ( np.pi * w0_laser * np.sqrt( 1 + (Z_values * theta / w0_laser)**2 ) )
w_1 = w_0
T_values = ( 2 * w_1*w_2 / ( w_1**2 + w_2**2 ) )**2

plt.figure(figsize=(8, 5))
plt.plot(Z_values, T_values, label="Efficacité de couplage", color='b')
plt.axvline(Z, color='r', linestyle='--', label=f"Z optimal = {Z*100:.2f} cm")
plt.xlabel("Distance Z [m]")
plt.ylabel("Efficacité de couplage T [-]")
plt.title("Efficacité de couplage en fonction de la distance Z")
plt.ylim(0, 1.1)
plt.xlim(0, 1.6)
plt.legend()
plt.grid()
plt.show()