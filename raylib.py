# Imports
import numpy as np

# Declarations
class ray_object(): pass
class sphere(ray_object): pass
class plane(ray_object): pass

# Classes
class ray_object:
    def __init__(self) -> None:
        pass
    
    def intersect(self, ray_origin:np.ndarray, ray_dir:np.ndarray) -> list:
        """
        Calculate if a ray intersects this object.
        Returns an array with False if no intersection was found [False]
        And an array with True and one or more values, v, that: ray_origin + v * ray_dir = hit
        """
        pass

class sphere (ray_object):
    def __init__(self, position:np.ndarray, radius:float) -> None:
        self.position = np.array(position, np.float32)
        self.radius = radius
    
    # https://www.scratchapixel.com/code.php?id=3&origin=/lessons/3d-basic-rendering/introduction-to-ray-tracing
    def intersect(self, ray_origin:np.ndarray, ray_dir:np.ndarray) -> list:
        l = self.position - ray_origin
        tca = np.dot(l, ray_dir)
        if (tca < 0): return [False]
        d2 = np.dot(l, l) - tca * tca
        if (d2 > self.radius): return [False]
        thc = np.sqrt(self.radius - d2)
        return [True, tca - thc, tca + thc]

class plane (ray_object):
    def __init__(self, position:np.ndarray, normal:np.ndarray) -> None:
        self.position = np.array(position, np.float32)
        self.normal = np.array(normal, np.float32)

    # http://lousodrome.net/blog/light/2020/07/03/intersection-of-a-ray-and-a-plane/
    def intersect(self, ray_origin: np.ndarray, ray_dir: np.ndarray) -> list:
        den = np.dot(ray_dir, self.normal)
        if (den == 0): return [False]
        t = np.dot((self.position - ray_origin), self.normal) / np.dot(ray_dir, self.normal)
        if (t < 0): return False
        return [True, t]

if __name__ == "__main__":
    # s = sphere([2, 5, 0], 1)
    # print(s.intersect([0, 0, 0], [1, 0, 0]))
    p = plane([0, 0, 0], [0, 1, 0])
    print(p.intersect([0, -2, 0], [0, 0, 2]))

