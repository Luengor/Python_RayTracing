## Imports
from raylib import *
import numpy as np
import math
import cv2

## Constants
SIZE = 1024, 1024
FOV = 90
NORMAL_BUMP = 2e-5

## Global variables
fov2px = math.tan(math.pi * 0.5 * FOV / 180) / (SIZE[0] - 1)
image = np.zeros(shape=(SIZE[1], SIZE[0], 3), dtype=np.uint8)

## Scene variables
cam = camera(vector(0, 1, 0), vector(0, 0, 1), vector(0, 1, 0), vector(1, 0, 0))
objects = [sphere(vector(0.5, 1, 3), 0.2, color=[200, 100, 100]),
           sphere(vector(-0.5, 1, 3), 0.01, color=[100, 100, 200]),
           plane(vector(0, 0, 0), vector(0, 1, 0), color=[110, 170, 110])]
lights = [light(vector(0, 3, 3), 2)]
sky_color = [50, 50, 50]

## Sines calculations
# We actually only need half of them, as they can be reused
x_sines = [math.sin((x - SIZE[0] * 0.5 + 0.5) * fov2px) for x in range(SIZE[0])]
y_sines = [math.sin(-(y - SIZE[1] * 0.5 + 0.5) * fov2px) for y in range(SIZE[1])]

## Main loop
for y in range(SIZE[1]):
    for x in range(SIZE[0]):
        ## Calculate the ray
        r = ray(cam.position, cam.fordward + cam.up*y_sines[y] + cam.right*x_sines[x])

        ## Get the closer hit
        hit = rayhit(distance=math.inf)
        hitter = -1
        for o in range(len(objects)):
            new_hit = objects[o].intersect(r)
            if new_hit.distance >= 0 and new_hit.distance < hit.distance:
                hit = new_hit
                hitter = o
        
        ## Draw sky color if no hits
        if hitter == -1:
            image[y, x, :] = sky_color
            continue

        ## Check if the point is in shadow
        r = ray(hit.position + (hit.normal * NORMAL_BUMP))
        r.direction = (lights[0].position - r.origin).normalize()

        shadow = False
        for obj in objects:
            if obj.intersect(r).distance >= 0:
                shadow = True
                break

        ## Draw black-er color when in shadow
        if shadow:
            image[y, x, :] = np.subtract(objects[hitter].color, [100, 100, 100])
        else:
            image[y, x, :] = objects[hitter].color

cv2.imwrite("something.png", image)
