## Imports
from raylib import *
import numpy as np
import math
import cv2

## Constants
SIZE = 1280, 720
FOV = 90
NORMAL_BUMP = 2e-5

## Global variables
fov2px = math.tan(math.pi * 0.5 * FOV / 180) / (SIZE[0] - 1)
image = np.zeros(shape=(SIZE[1], SIZE[0], 3), dtype=np.uint8)

## Scene variables
cam = camera(vector(0, 1, 0), vector(0, 0, 1), vector(0, 1, 0), vector(1, 0, 0))
objects = [sphere(vector(-1.2, 1, 5), 0.8, color=[255, 100, 255], diffuse_coeff=1.5),
           sphere(vector(1.2, 1, 5), 0.8, color=[100, 255, 255], shading=ray_object.SHADING_SPECULAR, specular_coeff=2.5, specular_p=2),
           plane(vector(0, 0, 0), vector(0, 1, 0), color=[200, 200, 200], shading=ray_object.SHADING_NONE)]
lights = [light(vector(0, 2, 2), 3)]
sky_color = [200, 200, 200]

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

        ## Lighting
        color = np.array([0, 0, 0], dtype=np.int16)
        r = ray(hit.position + (hit.normal * NORMAL_BUMP))

        for l in range(len(lights)):
            r.direction = (lights[l].position - r.origin).normalize()
            r.max_squared_distance = (lights[l].position - r.origin).magnitude2
            
            shadow = False
            for o in range(len(objects)):
                if objects[o].intersect(r).distance >= 0:
                    shadow = True
                    break
            if not shadow:
                light_intensity = lights[l].strength / r.max_squared_distance

                match objects[hitter].shading:
                    case ray_object.SHADING_NONE:
                        color = objects[hitter].color

                    case ray_object.SHADING_DIFFUSE:
                        ld = objects[hitter].diffuse_coeff * light_intensity * max(0, hit.normal*r.direction)
                        color += [int(c * ld) for c in objects[hitter].color]
                        
                    case ray_object.SHADING_SPECULAR:
                        camera_header = (cam.position - hit.position).normalize()
                        h = (camera_header + r.direction) / ((camera_header + r.direction).magnitude)
                        ls = objects[hitter].specular_coeff * light_intensity * math.pow(max(0, hit.normal * h), objects[hitter].specular_p)
                        color += [int(c * ls) for c in objects[hitter].color]

        ## Draw the point
        image[y, x, :] = np.clip(color, 0, 255)
        
cv2.imwrite("shading.png", image)
