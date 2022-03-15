# Imports
from raylib import *
import cv2

# Constants
SIZE = 1280, 720
FOV = 90

# Scene
world = Scene()
world.skycolor = Vector(255, 200, 200)
world.objects += [
    Sphere(Vector(-1.1, 1, 10), 1, Surface(Vector(255, 100, 255), Surface.SHADING_DIFFUSE, diffuse_coeff=1.5)),
    Sphere(Vector(1.1, 1, 10), 1, Surface(Vector(100, 255, 255), Surface.SHADING_SPECULAR, specular_coeff=2, specular_p=1.2)),
    Plane(Vector(0, 0, 0), Vector(0, 1, 0), Surface(Vector(200, 200, 200), Surface.SHADING_REFLECTIVE))
]
world.lights += [DirectionalLight(Vector(-0.4, -1 , 1), 0.8)]
world.camera.set(position=Vector(0, 0.7, 0), fordward=Vector(0, 0, 1), up=Vector(0, 1, 0), right=Vector(1, 0, 0), size=SIZE, fov=FOV, sample_size=4)

# Render
cv2.imwrite("SSAA.png", world.camera.render())