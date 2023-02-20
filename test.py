
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import LinearSegmentedColormap

# Define the diffusion coefficient and time step
D = 0.2
dt = 1
K_max = 100
a = 5
C_50 = 0.5

# Create a 100x100 matrix with initial pollution concentration
C = np.zeros((100, 100))
C[random.randint(0,99), random.randint(0,99)] = 2000

# Simulate pollution diffusion using the explicit method
for t in np.arange(0, 365, dt):
    C[1:-1, 1:-1] += D*dt*(C[2:, 1:-1] - 2*C[1:-1, 1:-1] + C[:-2, 1:-1] +
                            C[1:-1, 2:] - 2*C[1:-1, 1:-1] + C[1:-1, :-2])

C = np.subtract(1, C)

K = K_max / (1 + np.exp(-a*(C - C_50)))

print(np.max(C))
print(np.max(K))


# # Plot the concentration matrix
# plt.imshow(C, cmap='winter')
# plt.colorbar()
# plt.show()



cmap_colors = [(255/255,255/255,102/255), (3/255,129/255,102/255)]
custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", cmap_colors)
# # Plot the environmental tolerance matrix
C_map = plt.imshow(C, cmap='viridis')
C_colorbar = plt.colorbar(C_map)
C_colorbar.set_label('Pollution Concentration')
plt.show()

K_map = plt.imshow(K, cmap='winter')
K_colorbar = plt.colorbar(K_map)
K_colorbar.set_label('Environmental capacity after contamination')
plt.show()