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

angle_prisme = np.arange(0, 190, 10)

intensite_transmise = np.array([153, 142.5, 128.5, 106.7, 81.8, 53.9,
                                30.2, 12.9, 1.8, 1.6, 11.1, 31.7,
                                57.3, 90.7, 124.2, 156.5, 180.5, 191.0, 197.5])

##erreur_y = np.array([1, 0.5, 0.5, 0.5, 0.5, 0.5,
##                     0.2, 0.1, 0.1, 0.1, 0.1, 0.1,
##                     0.3, 0.3, 0.5, 0.8, 0.5, 0.8, 0.8])

ax2.plot(angle_prisme, intensite_transmise)

# Caratérisation des lames à retard
fig3 = plt.figure()
ax3 = fig3.add_subplot(1, 1, 1)
ax3.xaxis.set_minor_locator(tck.AutoMinorLocator())
ax3.yaxis.set_minor_locator(tck.AutoMinorLocator())

angle_polariseur = np.arange(0, 190, 20)

intensite_demi_22_5 = np.array([55.9, 123.3, 172.1, 199.6, 181.2,
                                108.0, 47.9, 4.0, 8.0, 53.1])

intensite_demi_45 = np.array([21.1, 0.1, 24.7, 84.1, 158.6,
                              189.03, 190.7, 138.1, 78.1, 19.1])

intensite_quart_22_5 = np.array([38.5, 74.8, 114.4, 138.3, 143.7,
                                 102.0, 61.5, 26.2, 18.1, 37.4])

intensite_quart_45 = np.array([90.3, 90.8, 93.7, 92.4, 95.6,
                               83.0, 80.3, 76.3, 84.4, 86.10])

ax3.plot(angle_polariseur, intensite_demi_22_5,
         angle_polariseur, intensite_demi_45, '--',
         angle_polariseur, intensite_quart_22_5, '-.',
         angle_polariseur, intensite_quart_45, ':')


##angle = np.arange(0, 200, 20)
##I_demi_22_5 = np.array([55.9, 123.3, 172.1, 199.6,
##                        181.2, 108.0, 47.9, 4.0,
##                        8.0, 53.1])
##plt.plot(angle, I_demi_22_5)
plt.show()
