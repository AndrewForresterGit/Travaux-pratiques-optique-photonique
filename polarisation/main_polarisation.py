import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck




# Polarisation par réflexion
fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)
ax1.xaxis.set_minor_locator(tck.AutoMinorLocator())
ax1.yaxis.set_minor_locator(tck.AutoMinorLocator())

angle_incident = np.arange(10, 85, 5)

intensite_TE = np.array([18.6, 17.5, 16.1, 14.3, 12.2,
                         9.6, 6.6, 3.7, 1.2, 0.1,
                         2.1, 10.4, 32.1, 83.7, 162])

intensite_TM = np.array([19.5, 21.4, 22.9, 24.4, 29.7,
                         31.7, 41.7, 51.6, 63.5, 80.8,
                         104.4, 131.2, 172.0, 239, 339])

ax1.plot(angle_incident, intensite_TE,
        angle_incident, intensite_TM, '--')
ax1.axhline(0, color='gray', linestyle=':', linewidth=1)
ax1.axvline(0, color='gray', linestyle=':', linewidth=1)
#ax1.set_title("Intensité réfléchie en fonction de l'angle d'incidence du laser")
ax1.set_ylabel(r"Intensité [$\mu$A]")
ax1.set_xlabel("Angle d'incidence")
I_max_ax1 = 250  
#ax1_right = ax1.twinx()
#ax1_right.set_ylabel('Transmission [%]')
#ax1_right.set_ylim(0, (ax1.get_ylim()[1] / I_max_ax1) * 100)
#ax1_right.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))

ax1.xaxis.set_major_locator(tck.MultipleLocator(10))
ax1.yaxis.set_major_locator(tck.MultipleLocator(50))  
ax1.grid(True, which='major', linestyle=':', linewidth=0.5)


'''
Graphiquement, on voit que l'angle de Brewster du plexiglas est 55°.
Cette valeur est ±1° de la valeur théorique.
'''

# Caractérisation du prisme de Glan-Thompson et du polariseur dichroïque

# Vérification de la loi de Malus
fig2 = plt.figure()
ax2 = fig2.add_subplot(1, 1, 1)
ax2.xaxis.set_minor_locator(tck.AutoMinorLocator())
ax2.yaxis.set_minor_locator(tck.AutoMinorLocator())
ax2.axhline(0, color='gray', linestyle=':', linewidth=1)
ax2.axvline(0, color='gray', linestyle=':', linewidth=1)
#ax2.set_title("Intensité en fonction de l'angle du prisme de Glan-Thompson")
ax2.xaxis.set_major_locator(tck.MultipleLocator(30))
ax2.yaxis.set_major_locator(tck.MultipleLocator(25))  
ax2.grid(True, which='major', linestyle=':', linewidth=0.5)


angle_prisme = np.arange(0, 190, 10)

intensite_transmise = np.array([153, 142.5, 128.5, 106.7, 81.8, 53.9,
                                30.2, 12.9, 1.8, 1.6, 11.1, 31.7,
                                57.3, 90.7, 124.2, 156.5, 180.5, 191.0, 197.5])

##erreur_y = np.array([1, 0.5, 0.5, 0.5, 0.5, 0.5,
##                     0.2, 0.1, 0.1, 0.1, 0.1, 0.1,
##                     0.3, 0.3, 0.5, 0.8, 0.5, 0.8, 0.8])

ax2.plot(angle_prisme, intensite_transmise)
I_max_ax2 = 315  
ax2_right = ax2.twinx()
ax2_right.set_ylabel('Transmission [%]')
ax2_right.set_ylim(0, (ax2.get_ylim()[1] / I_max_ax2) * 100)
ax2_right.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax2.set_xlabel(r'Angle du polariseur [$\degree$]')
ax2.set_ylabel(r'Amplitude [$\mu$A]')

# Caratérisation des lames à retard
fig3 = plt.figure()
ax3 = fig3.add_subplot(1, 1, 1)
ax3.xaxis.set_minor_locator(tck.AutoMinorLocator())
ax3.yaxis.set_minor_locator(tck.AutoMinorLocator())
ax3.axhline(0, color='gray', linestyle=':', linewidth=1)
ax3.axvline(0, color='gray', linestyle=':', linewidth=1)
#ax3.set_title("Intensité du laser transmise à travers un polariseur (Glan-Thompson ou dichroïque) en fonction de son angle pour différentes orientations d’une lame à retard (22,5° et 45°).", wrap=True)
ax3.set_xlabel(r'Angle du polariseur [$\degree$]')
ax3.set_ylabel(r'Amplitude [$\mu$A]')
ax3.xaxis.set_major_locator(tck.MultipleLocator(30))
ax3.yaxis.set_major_locator(tck.MultipleLocator(25))  
ax3.grid(True, which='major', linestyle=':', linewidth=0.5)



angle_polariseur = np.arange(0, 190, 20)

intensite_demi_22_5 = np.array([55.9, 123.3, 172.1, 199.6, 181.2,
                                108.0, 47.9, 4.0, 8.0, 53.1])

intensite_demi_45 = np.array([21.1, 0.1, 24.7, 84.1, 158.6,
                              189.03, 190.7, 138.1, 78.1, 19.1])

intensite_quart_22_5 = np.array([38.5, 74.8, 114.4, 138.3, 143.7,
                                 102.0, 61.5, 26.2, 18.1, 37.4])

intensite_quart_45 = np.array([90.3, 90.8, 93.7, 92.4, 95.6,
                               83.0, 80.3, 76.3, 84.4, 86.10])

ax3.plot(angle_polariseur, intensite_demi_22_5, label="Lame demi onde 22,5°")
ax3.plot(angle_polariseur, intensite_demi_45, '--', label="Lame à demi onde 45°")
ax3.plot(angle_polariseur, intensite_quart_22_5, '-.', label="Lame quart d'onde 22,5°")
ax3.plot(angle_polariseur, intensite_quart_45, ':', label="Lame quart d'onde 45°")
ax3.legend(loc="best")

I_max_ax3 = 315  
ax3_right = ax3.twinx()
ax3_right.set_ylabel('Transmission [%]')
ax3_right.set_ylim(0, (ax3.get_ylim()[1] / I_max_ax3) * 100)
ax3_right.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))

##angle = np.arange(0, 200, 20)
##I_demi_22_5 = np.array([55.9, 123.3, 172.1, 199.6,
##                        181.2, 108.0, 47.9, 4.0,
##                        8.0, 53.1])
##plt.plot(angle, I_demi_22_5)
plt.show()
