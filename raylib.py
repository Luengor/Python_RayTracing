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
class Light(): pass
class Camera(): pass
# Others
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

    def __mul__(self, other) -> Vector:
        if isinstance(other, Vector):
            return Vector.dot(self, other)
        elif isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)
    
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
    def __init__(self, position:Vector, strength:float) -> None:
        self.position = position
        self.strength = strength


class Camera:
    """
        Main rendering class
    """
    def __init__(self, world:Scene, position:Vector=Vector(), fordward:Vector=Vector(),
            up:Vector=Vector(), right:Vector=Vector(), **kwargs) -> None:
        self.world = world
        self.position = position
        self.fordward = fordward
        self.up = up
        self.right = right
        
        self.fov = 90
        self.size = [1280, 720]
        self.normal_bump:float=2e-5
        self.set(**kwargs)

    def set(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def cast(self, r:Ray) -> List[int, int, int]:
        """
            Casts a ray and returns a list containing the color of the point
        """
        color = Vector()
        ## Get the closer hit
        hit = RayHit(distance=math.inf)
        hitter = -1
        for o in range(len(self.world.objects)):
            new_hit = self.world.objects[o].intersect(r)
            if new_hit.distance >= 0 and new_hit.distance < hit.distance:
                hit = new_hit
                hitter = o
        
        ## Draw sky color if no hits
        if hitter == -1:
            color.set(self.world.skycolor)
            return color

        ## Lighting
        r = Ray(hit.position + (hit.normal * self.normal_bump))

        for l in range(len(self.world.lights)):
            r.direction = (self.world.lights[l].position - r.origin).normalize()
            r.max_squared_distance = (self.world.lights[l].position - r.origin).magnitude2
            
            # Loop through all lights to check if we are in complete shadow
            # Never mind, I am just dumb
            shadow = False
            for o in range(len(self.world.objects)):
                if self.world.objects[o].intersect(r).distance >= 0:
                    shadow = True
                    break
            
            # If the point isn't in shadow, calculate the lighting
            if not shadow:
                light_intensity = self.world.lights[l].strength / r.max_squared_distance
                surf = self.world.objects[hitter].surface
                match surf.shading:
                    case Surface.SHADING_NONE:
                        color = surf.color

                    case Surface.SHADING_FLAT:
                        color = surf.color * light_intensity * surf.flat_coeff

                    case Surface.SHADING_DIFFUSE:
                        ld = surf.diffuse_coeff * light_intensity * max(0, hit.normal*r.direction)
                        color += [int(c * ld) for c in surf.color]
                        
                    case Surface.SHADING_SPECULAR:
                        # This works weird when the light is really close
                        camera_header = (self.position - hit.position).normalize()
                        h = (camera_header + r.direction) / ((camera_header + r.direction).magnitude)
                        ls = surf.specular_coeff * light_intensity * math.pow(max(0, hit.normal * h), surf.specular_p)
                        color += [int(c * ls) for c in surf.color]
        
        return list(map(lambda c: int(min(c, 255)), color.list))

    def render(self) -> np.ndarray:
        """
            Renders the scene casting a series of rays according to the fov and size
            variables.
            Returns a numpy array with the image data
        """
        # Pre calcs
        image = np.zeros(shape=(self.size[1], self.size[0], 3), dtype=np.uint8)
        fov2px = math.tan(math.pi * 0.5 * self.fov / 180) / (self.size[0] - 1)
        x_sines = [math.sin((x - self.size[0] * 0.5 + 0.5) * fov2px) for x in range(self.size[0])]
        y_sines = [math.sin(-(y - self.size[1] * 0.5 + 0.5) * fov2px) for y in range(self.size[1])]

        # render loop
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                r = Ray(self.position, self.fordward + self.up*y_sines[y] + self.right*x_sines[x])
                image[y, x, :] = list(self.cast(r))
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

    def __init__(self, color:Vector=Vector(255, 255, 255), shading:int=0, **kwargs) -> None:
        self.color = color
        self.shading = shading
        self.flat_coeff = 1
        self.diffuse_coeff = 1
        self.specular_coeff = 1
        self.specular_p = 1

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
