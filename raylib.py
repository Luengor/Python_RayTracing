# Imports
from __future__ import annotations
import math

# Declarations
class vector(): pass
class rayhit(): pass
class ray(): pass
class ray_object(): pass
class sphere(ray_object): pass
class plane(ray_object): pass
class light(): pass
class camera(): pass

# Small functions
def div(a, b) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        return (-1 * (a < 0)) * float('inf')

# Classes
class vector:
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

    def set(self, v:vector) -> None:
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
        return vector.dot(self, self)

    ## Functions
    def normalize(self) -> vector:
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
    
    def dot(v:vector, w:vector) -> float:
        """
            Calculates the dot product of 2 vectors.
        """
        return v.x*w.x + v.y*w.y + v.z*w.z

    ## Overloads
    def __add__(self, other) -> vector:
        if isinstance(other, vector):
            return vector(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (int, float)):
            return vector(self.x + other, self.y + other, self.z + other)
    
    def __sub__(self, other) -> vector: # duplicate code :(
        if isinstance(other, vector):
            return vector(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (int, float)):
            return vector(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other) -> vector:
        if isinstance(other, vector):
            return vector.dot(self, other)
        elif isinstance(other, (int, float)):
            return vector(self.x * other, self.y * other, self.z * other)
    
    def __truediv__(self, other) -> vector:
        if isinstance(other, vector):
            return vector(div(self.x, other.x), div(self.y, other.y), div(self.z, other.z))
        elif isinstance(other, (int, float)):
            return self * (1 / other)

    def __getitem__(self, item:int) -> float:
        return getattr(self, "xyz"[item])

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

class rayhit():
    def __init__(self, position:vector=None, normal:vector=None, distance:float = -1) -> None:
        self.position = position
        self.normal = normal
        self.distance = distance
    
    def __str__(self) -> str:
        return f"{self.position} {self.normal} {self.distance}"

class ray():
    def __init__(self, origin:vector=vector(), direction:vector=vector(), max_squared_distance:float=math.inf) -> None:
        self.origin = origin
        self.direction = direction
        self.direction.normalize()
        self.max_squared_distance = max_squared_distance

    def position_at(self, x:float) -> vector:
        return (self.origin + (self.direction * x))

class ray_object:
    def __init__(self) -> None:
        self.color = [255, 255, 255]
    
    def intersect(self, r:ray) -> rayhit:
        """
        Calculate if a ray intersects this object.
        Returns an array with the hit and the normal. 
        """
        pass

class sphere (ray_object):
    def __init__(self, position:vector, radius:float, **kwargs) -> None:
        super().__init__()
        self.position = position
        self.radius = radius

        for key, value in kwargs.items():
            setattr(self, key, value)

    # https://www.scratchapixel.com/code.php?id=3&origin=/lessons/3d-basic-rendering/introduction-to-ray-tracing
    def intersect(self, r:ray) -> rayhit:
        l = self.position - r.origin
        tca = l * r.direction
        if (tca < 0): return rayhit()
        d2 = l*l - tca*tca
        if (d2 > self.radius): return rayhit()

        thc = math.sqrt(self.radius - d2)
        dis = (tca - thc)
        if (dis*dis > r.max_squared_distance): return rayhit()
        hit = rayhit(r.position_at(dis))
        hit.normal = (hit.position - self.position).normalize()
        hit.distance = dis
        return hit

class plane (ray_object):
    def __init__(self, position:vector, normal:vector, **kwargs) -> None:
        super().__init__()
        self.position = position
        self.normal = normal

        for key, value in kwargs.items():
            setattr(self, key, value)

    # http://lousodrome.net/blog/light/2020/07/03/intersection-of-a-ray-and-a-plane/
    def intersect(self, r:ray) -> rayhit:
        den = r.direction * self.normal
        if (den == 0): return rayhit()
        t = div((self.position - r.origin) * self.normal, r.direction * self.normal)
        if (t < 0): return rayhit()

        if (t*t > r.max_squared_distance): return rayhit()
        hit = rayhit(r.position_at(t), self.normal, t)
        return hit

class light:
    def __init__(self, position:vector, strength:float) -> None:
        self.position = position
        self.strength = strength

class camera:
    def __init__(self, position:vector, fordward:vector=vector(), up:vector=vector(), right:vector=vector()) -> None:
        self.position = position
        self.fordward = fordward
        self.up = up
        self.right = right


if __name__ == "__main__":
    v = vector(1, 2, 3)
    print(v / 2)
