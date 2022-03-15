## Imports
from __future__ import annotations
from typing import List
import numpy as np
import math

## Declarations
# Types
class Vector(): pass
# Ray
class RayHit(): pass
class Ray(): pass
# Objects
class RayObject(): pass
class Sphere(RayObject): pass
class Plane(RayObject): pass
# Lights
class Light(): pass
class PointLight(Light): pass
class DirectionalLight(Light): pass
# Others
class Camera(): pass
class Scene(): pass
class Surface(): pass


## Small functions
def div(a, b) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        return (-1 * (a < 0)) * float('inf')

## Classes

class Vector:
    """
    ## Custom class because it's faster and convenient
    """
    ## Seters
    def __init__(self, x:float=0, y:float=0, z:float=0, mag:float=-1) -> None:
        """
            Initiates the vector
            The mag variable is used internally to keep track of the magnitude
            of the vector to reuse it whenever possible. So, don't touch / don't
            give it a random value or calculations will fail.
        """
        self.x = x
        self.y = y
        self.z = z

        self.mag = -1
        """ The pre-computed magnitude. """

    def set(self, v:Vector) -> None:
        """
            Copy the values of another vector
        """
        self.__init__(v.x, v.y, v.z, v.mag)

    ## Properties
    @property
    def magnitude(self) -> float:
        """
            The calculated magnitude of the vector. It can be reused with .mag
        """
        self.mag = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        return self.mag

    @property
    def magnitude2(self) -> float:
        """
            The squared magnitude of the vector.
        """
        return Vector.dot(self, self)

    @property
    def list(self) -> List[int]:
        return [self.x, self.y, self.z]


    ## Functions
    def normalize(self) -> Vector:
        """
            Normalizes the vector and returns it
        """
        if self.magnitude != 1:
            if self.mag == 0:
                self.x = math.inf
                self.y = math.inf
                self.z = math.inf
            else:
                self.x /= self.mag
                self.y /= self.mag
                self.z /= self.mag
        return self
    
    def dot(v:Vector, w:Vector) -> float:
        """
            Calculates the dot product of 2 vectors.
        """
        return v.x*w.x + v.y*w.y + v.z*w.z

    def rgb(self) -> None:
        self.x = min(self.x, 255)
        self.y = min(self.y, 255)
        self.z = min(self.z, 255)

    ## Overloads
    def __add__(self, other) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, list):
            return Vector(self.x + other[0], self.y + other[1], self.z + other[2])
        elif isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other, self.z + other)
    
    def __sub__(self, other) -> Vector: # duplicate code :(
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector.dot(self, other)
        elif isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, other):
        return self * other


    def __truediv__(self, other) -> Vector:
        if isinstance(other, Vector):
            return Vector(div(self.x, other.x), div(self.y, other.y), div(self.z, other.z))
        elif isinstance(other, (int, float)):
            return self * (1 / other)

    def __getitem__(self, item:int) -> float:
        return self.list[item]

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


class RayHit:
    """
        Container for hits position, normals and distance
    """
    def __init__(self, position:Vector=None, normal:Vector=None, distance:float = -1) -> None:
        self.position = position
        self.normal = normal
        self.distance = distance


class Ray:
    """
        Container for a ray. Made of two vectors and a float (origin, direction and max
        allowed distance)
    """
    def __init__(self, origin:Vector=Vector(), direction:Vector=Vector(), max_squared_distance:float=math.inf) -> None:
        self.origin = origin
        self.direction = direction
        self.direction.normalize()
        self.max_squared_distance = max_squared_distance

    def position_at(self, x:float) -> Vector:
        """
            Returns the point at the x point of the line:
            origin + direction * x
        """
        return (self.origin + (self.direction * x))


class RayObject:
    """
        Base class for all objects to render
    """
    def __init__(self) -> None:
        self.position = Vector()
        self.surface = Surface()
    
    def intersect(self, r:Ray) -> RayHit:
        """
        Calculate if a ray intersects this object.
        Returns a RayHit
        """
        pass


class Sphere (RayObject):
    """
        Sphere Ray Object.
    """
    def __init__(self, position:Vector, radius:float, s:Surface) -> None:
        super().__init__()
        self.position = position
        self.radius = radius
        self.surface = s

    # https://www.scratchapixel.com/code.php?id=3&origin=/lessons/3d-basic-rendering/introduction-to-ray-tracing
    def intersect(self, r:Ray) -> RayHit:
        l = self.position - r.origin
        tca = l * r.direction
        if (tca < 0): return RayHit()
        d2 = l*l - tca*tca
        if (d2 > self.radius): return RayHit()

        thc = math.sqrt(self.radius - d2)
        dis = (tca - thc)
        if (dis*dis > r.max_squared_distance): return RayHit()
        hit = RayHit(r.position_at(dis))
        hit.normal = (hit.position - self.position).normalize()
        hit.distance = dis
        return hit


class Plane (RayObject):
    """
        Infinite plane ray object
    """
    def __init__(self, position:Vector, normal:Vector, s:Surface) -> None:
        super().__init__()
        self.position = position
        self.normal = normal
        self.surface = s

    # http://lousodrome.net/blog/light/2020/07/03/intersection-of-a-ray-and-a-plane/
    def intersect(self, r:Ray) -> RayHit:
        den = r.direction * self.normal
        if (den == 0): return RayHit()
        t = div((self.position - r.origin) * self.normal, r.direction * self.normal)
        if (t < 0): return RayHit()

        if (t*t > r.max_squared_distance): return RayHit()
        hit = RayHit(r.position_at(t), self.normal, t)
        return hit


class Light:
    """
        Container for lights position and strength
    """
    LIGHT_DIRECTIONAL = 0
    LIGHT_POINT = 1

    def __init__(self, light_type:int) -> None:
        self.type = light_type


class PointLight (Light):
    def __init__(self, position:Vector, strength:float) -> None:
        super().__init__(Light.LIGHT_POINT)
        self.position = position
        self.strength = strength


class DirectionalLight (Light):
    def __init__(self, direction:Vector, strength:float) -> None:
        super().__init__(Light.LIGHT_DIRECTIONAL)
        self.direction = direction.normalize()
        self.strength = strength


class Camera:
    """
        Main rendering class
    """
    def __init__(self, world:Scene, position:Vector=Vector(), fordward:Vector=Vector(),
            up:Vector=Vector(), right:Vector=Vector(), fov:float=90, size:List[int, int] = [1280, 720],
            sample_size:int=1, normal_bump:float=2e-5, reflection_limit:int=1) -> None:
        """
            :param fov: Field of view of the camera
            :param size: Dimensions of the image generated in rendering
            :param sample_size: Number of samples for SSAA ( the number of
            samples will be sample_size^2 )
            :param normal_bump: Magnitude of a normal vector applied before the
            ray calculations to prevent false hits
            :param reflection_limit: Max number of reflections allowed

        """
        self.world = world
        self.position = position
        self.fordward = fordward
        self.up = up
        self.right = right
        self.fov = fov
        self.size = size
        self.sample_size = sample_size
        self.normal_bump = normal_bump
        self.reflection_limit = reflection_limit

    def set(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def cast(self, light_ray:Ray, reflection:int=1) -> Vector:
        """
            Casts a ray and returns a list containing the color of the point.
            (You souldn't use this)
        """
        color = Vector()
        ## Get the closer hit
        hit = RayHit(distance=math.inf)
        hitter = -1
        for o in range(len(self.world.objects)):
            new_hit = self.world.objects[o].intersect(light_ray)
            if new_hit.distance >= 0 and new_hit.distance < hit.distance:
                hit = new_hit
                hitter = o
        
        ## Draw sky color if no hits
        if hitter == -1:
            color.set(self.world.skycolor)
            return color

        ## Lighting
        light_ray = Ray(hit.position + (hit.normal * self.normal_bump))

        for l in range(len(self.world.lights)):
            if self.world.lights[l].type == Light.LIGHT_POINT: 
                light_ray.direction = (self.world.lights[l].position - light_ray.origin).normalize()
                light_ray.max_squared_distance = (self.world.lights[l].position - light_ray.origin).magnitude2
            else:
                light_ray.direction = self.world.lights[l].direction * -1
                light_ray.max_squared_distance = float('inf')
            

            # Loop through all lights to check if we are in complete shadow
            # Never mind, I am just dumb
            shadow = False
            for o in range(len(self.world.objects)):
                if self.world.objects[o].intersect(light_ray).distance >= 0:
                    shadow = True
                    break
            
            # If the point isn't in shadow, calculate the lighting
            if not shadow:
                if self.world.lights[l].type == Light.LIGHT_POINT:
                    light_intensity = self.world.lights[l].strength / light_ray.max_squared_distance
                else:
                    light_intensity = self.world.lights[l].strength
                
                surf = self.world.objects[hitter].surface
                match surf.shading:
                    case Surface.SHADING_NONE:
                        color = surf.color

                    case Surface.SHADING_FLAT:
                        color = surf.color * light_intensity * surf.flat_coeff

                    case Surface.SHADING_DIFFUSE:
                        ld = surf.diffuse_coeff * light_intensity * max(0, hit.normal*light_ray.direction)
                        color += [int(c * ld) for c in surf.color]
                        
                    case Surface.SHADING_SPECULAR:
                        # This works weird when the light is really close
                        camera_header = (self.position - hit.position).normalize()
                        h = (camera_header + light_ray.direction) / ((camera_header + light_ray.direction).magnitude)
                        ls = surf.specular_coeff * light_intensity * math.pow(max(0, hit.normal * h), surf.specular_p)
                        color += [int(c * ls) for c in surf.color]
                    
                    case Surface.SHADING_REFLECTIVE:
                        if reflection >= 0:
                            ld = surf.diffuse_coeff * light_intensity * max(0, hit.normal*light_ray.direction)
                            camera_header = (self.position - hit.position).normalize()
                            r = (hit.normal * camera_header) * hit.normal * 2  - camera_header
                            relfect = self.cast(Ray(hit.position + hit.normal * self.normal_bump, r), reflection - 1)
                            color += (relfect * ld * surf.reflective_coeff)
        
        color.rgb()
        return color

    def render(self) -> np.ndarray:
        """
            Renders the scene casting a series of rays according to the fov
            and size variables.
            :returns np.ndarray: Returns a numpy array with the image data.
        """
        # Pre calcs
        image = np.zeros(shape=(self.size[1], self.size[0], 3), dtype=np.uint8)
        fov2px = math.tan(math.pi * 0.5 * self.fov / 180) / (self.size[0] - 1)
        offset = 1 / (self.sample_size)
        
        # Main render loop
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                # Color init
                color = Vector()
                # Range through the samples
                for s in range(self.sample_size ** 2):
                    # Give an offset depending on the sample (basically rendering
                    # the image at a higher quality and then downscaling)
                    sx = s % self.sample_size
                    sy = s // self.sample_size
                    x_pos = (((x - offset*(.5 * (self.sample_size - 1))) + offset*sx) - self.size[0] * 0.5 + 0.5)
                    y_pos = (((y - offset*(.5 * (self.sample_size - 1))) + offset*sy) - self.size[1] * 0.5 + 0.5)
                    x_sine = (math.sin(+x_pos * fov2px))
                    y_sine = (math.sin(-y_pos * fov2px))
                    # Cast the ray and add the color
                    r = Ray(self.position, self.fordward + self.up*y_sine + self.right*x_sine)
                    color += self.cast(r, self.reflection_limit)
                
                image[y, x, :] = list(color / self.sample_size**2)
        return image


class Scene:
    def __init__(self) -> None:
        self.objects:List[RayObject] = []
        self.lights:List[Light] = []
        self.camera = Camera(self, Vector())
        self.skycolor = Vector(50, 50, 50)
        
    def set(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


class Surface:
    # Constants
    SHADING_NONE = 0
    SHADING_FLAT = 1
    SHADING_DIFFUSE = 2
    SHADING_SPECULAR = 3
    SHADING_REFLECTIVE = 4

    def __init__(self, color:Vector=Vector(255, 255, 255), shading:int=0, **kwargs) -> None:
        self.color = color
        self.shading = shading
        self.flat_coeff = 1
        self.diffuse_coeff = 1
        self.specular_coeff = 1
        self.specular_p = 1
        self.reflective_coeff = 1

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
