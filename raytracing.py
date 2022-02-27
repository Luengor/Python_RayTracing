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
camera = np.array([[0, 1, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=np.float32)
objects = [raylib.sphere([0.5, 1, 4], 0.2, color=[200, 100, 100]), raylib.sphere([-0.3, 1, 3], 0.01, color=[100, 100, 200])]
lights = [raylib.light([-2, 1, 3], 1)]
sky_color = [50, 50, 50]

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
        # Each element of the hits array is: [Id of the object hit, [hit0, hit1, ...]]
        hits = []
        for o in range(len(objects)):
            new_hits = objects[o].intersect(ray_origin, ray_dir)
            if len(new_hits) > 0:
                hits.append([o, new_hits])
        
        ## Draw sky color if no hits
        if len(hits) == 0:
            image[y, x, :] = sky_color
            continue

        ## Sort the hits to only draw the closer one
        hits.sort(key=lambda h: h[1][0], reverse=False)

        ## Check if the point is in shadow
        ray_origin = ray_origin + ray_dir * (hits[0][1][0] - 0.05)
        ray_dir = lights[0].position - ray_origin

        shadow = False
        for obj in objects:
            if len(obj.intersect(ray_origin, ray_dir)) > 0:
                shadow = True
                break

        ## Draw black-er color when in shadow
        # Shadows are working weird, I think?
        # In the first-shadows image, the red one shouldn't be all in shadow
        if shadow:
            image[y, x, :] = np.subtract(objects[hits[0][0]].color, [100, 100, 100])
        else:
            image[y, x, :] = objects[hits[0][0]].color

cv2.imwrite("something.png", image)
