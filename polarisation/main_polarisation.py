import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()#figsize=plt.figaspect(.5))
ax = fig.add_subplot(1, 1, 1)

# Polarisation par réflexion
angle_incident = np.arange(10, 85, 5)
intensite_TE = np.array([18.6, 17.5, 16.1,
                         14.3, 12.2, 9.6,
                         6.6, 3.7, 1.2,
                         0.1, 2.1, 10.4,
                         32.1, 83.7, 162])
intensite_TM = np.array([19.5, 21.4, 22.9,
                         24.4, 29.7, 31.7,
                         41.7, 51.6, 63.5,
                         80.8, 104.4, 131.2,
                         172.0, 239, 339])


ax.plot(angle_incident, intensite_TE,
        angle_incident, intensite_TM, '--')



##angle = np.arange(0, 200, 20)
##I_demi_22_5 = np.array([55.9, 123.3, 172.1, 199.6,
##                        181.2, 108.0, 47.9, 4.0,
##                        8.0, 53.1])
##plt.plot(angle, I_demi_22_5)
plt.show()
