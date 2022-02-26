## Imports
import numpy as np
import raylib
import cv2

## Global variables
size = 1024, 1024
fov = 90    # It actually was broken, but I have no idea if this is correct now :)
fov2px = np.tan(np.pi * 0.5 * fov / 180) / (size[0] - 1)
image = np.zeros(shape=(size[1], size[0], 3), dtype=np.uint8)

## Scene variables
# Where the vectors of the camera are: Position, Fordward, Up, Right
camera = np.array([[0, 1, 0], [0, -0.2, 1], [0, 1, 0], [1, 0, 0]], dtype=np.float32)
objects = [raylib.sphere([1, 1, 5], 1), raylib.plane([0, 0, 0], [0, 1, 0]), raylib.aabb([-0.25, 0, 2.25], [-0.75, 1, 2.75])]

## Sines calculations
# We actually only need half of them, as they can be reused
x_sines = np.array(np.sin([(x - size[0] * 0.5 + 0.5) * fov2px for x in range(size[0])]), dtype=np.float32)
y_sines = np.array(np.sin([-(y - size[1] * 0.5 + 0.5) * fov2px for y in range(size[1])]), dtype=np.float32)

## Main loop
for y in range(size[1]):
    for x in range(size[0]):
        ## Calculate the ray
        ray_origin = camera[0]
        ray_dir = np.array(camera[1] + y_sines[y] * camera[2] + x_sines[x] * camera[3], dtype=np.float32)
        ray_dir /= np.linalg.norm(ray_dir)

        ## Get all hits
        hits = []
        for o in range(len(objects)):
            new_hits = objects[o].intersect(ray_origin, ray_dir)
            if len(new_hits) > 0:
                hits.append([o, new_hits])
        
        ## Draw the closer hit by sorting them
        for hit in sorted(hits, key=lambda h: h[1][0], reverse=True):
            if isinstance(objects[hit[0]], raylib.sphere):
                image[y, x, :] = [200, 100, 100]
            elif isinstance(objects[hit[0]], raylib.plane):
                image[y, x, :] = [100, 200, 100]
            else:
                image[y, x, :] = [100, 100, 200]
                
cv2.imwrite("something.png", image)
