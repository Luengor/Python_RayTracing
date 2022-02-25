## Imports
import numpy as np
import raylib
import cv2

## Global variables
size = 100, 60
fov = 60 * np.pi / 180
fov2px = fov / (size[0] - 1)
ray_matrix = np.ones(shape=(2, size[0], size[1]), dtype=np.float32)
image = np.array()

## Ray matrix calculation (so if I need more than an image, I can reuse this)
for y in range(size[1]):
    for x in range(size[0]):
        ray_matrix[0, x, y] = (x - size[0] * 0.5 + 0.5) * fov2px
        ray_matrix[1, x, y] = (y - size[1] * 0.5 + 0.5) * fov2px

