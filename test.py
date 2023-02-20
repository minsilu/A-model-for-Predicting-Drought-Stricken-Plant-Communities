
import numpy as np
import matplotlib.pyplot as plt
import random
import numpy as np

# Create a 100x100 matrix filled with zeros
matrix = np.zeros((100, 100))


percentage = 0.9
num_points = int(percentage * matrix.size)
indices = np.random.choice(range(matrix.size), num_points, replace=False)

matrix.flat[indices] = random.randint(300, 600)

matrix.flat[np.setdiff1d(range(matrix.size), indices)] = random.randint(600, 1200)


print(np.max(matrix))
print(np.min(matrix))

C_map = plt.imshow(matrix , cmap='viridis')
C_colorbar = plt.colorbar(C_map)
C_colorbar.set_label('Pollution Concentration')
plt.show()

