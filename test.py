import numpy as np
import matplotlib.pyplot as plt

# # create a 10x10 matrix with random values between 0 and 50
# my_matrix = np.random.randint(0, 51, size=(10, 10))

# # plot the matrix as a heat map
# plt.imshow(my_matrix, cmap='hot')

# # set the horizontal and vertical labels
# plt.xticks(np.arange(0, 10, step=1), np.arange(1000, 0, step= -100))
# plt.yticks(np.arange(0, 10, step=1), np.arange(1, 11, step=1))

# # add a colorbar to the plot with a label
# cbar = plt.colorbar()
# cbar.ax.set_ylabel('Color Depth')

# # display the plot
# plt.show()

biomass_matrix = np.random.rand(10, 10)
for i in range(10):
    for j in range(10):
        biomass_matrix[i, j] =  j
print(biomass_matrix)
    
part1 = biomass_matrix[:, :3]
part2 = biomass_matrix[:, 3:7]
part3 = biomass_matrix[:, 7:]

start = [100,400,800]
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4))

for i, part in enumerate([part1, part2, part3]):
    im = axes[i].imshow(part, cmap='hot')
    axes[i].set_xticks(np.arange(0, part.shape[1], step=1))
    axes[i].set_xticklabels(np.arange(start[i], part.shape[1]*100 + start[i] , step= 100))
    axes[i].set_yticks(np.arange(0, part.shape[0], step=1))
    axes[i].set_yticklabels(np.arange(1 , 11, step= 1))
    cbar = axes[i].figure.colorbar(im, ax=axes[i])
    cbar.ax.set_ylabel('Color Depth')

# 调整子图布局和间距
fig.tight_layout(pad=3.0)

# 显示热图
plt.show()



