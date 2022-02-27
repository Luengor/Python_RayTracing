# Imports
import numpy as np

# Declarations
class ray_object(): pass
class sphere(ray_object): pass
class plane(ray_object): pass
class aabb(ray_object): pass
class light(): pass

# Classes
class ray_object:
    def __init__(self) -> None:
        self.color = [255, 255, 255]
    
    def intersect(self, ray_origin:np.ndarray, ray_dir:np.ndarray) -> list:
        """
        Calculate if a ray intersects this object.
        Returns an array with the hits. 
        """
        pass

class sphere (ray_object):
    def __init__(self, position:np.ndarray, radius:float, **kwargs) -> None:
        super().__init__()
        self.position = np.array(position, np.float32)
        self.radius = radius

        for key, value in kwargs.items():
            setattr(self, key, value)

    # https://www.scratchapixel.com/code.php?id=3&origin=/lessons/3d-basic-rendering/introduction-to-ray-tracing
    def intersect(self, ray_origin:np.ndarray, ray_dir:np.ndarray) -> list:
        l = self.position - ray_origin
        tca = np.dot(l, ray_dir)
        if (tca < 0): return []
        d2 = np.dot(l, l) - tca * tca
        if (d2 > self.radius): return ([])
        thc = np.sqrt(self.radius - d2)
        return [tca - thc, tca + thc]

class plane (ray_object):
    def __init__(self, position:np.ndarray, normal:np.ndarray, **kwargs) -> None:
        super().__init__()
        self.position = np.array(position, np.float32)
        self.normal = np.array(normal, np.float32)

        for key, value in kwargs.items():
            setattr(self, key, value)

    # http://lousodrome.net/blog/light/2020/07/03/intersection-of-a-ray-and-a-plane/
    def intersect(self, ray_origin: np.ndarray, ray_dir: np.ndarray) -> list:
        den = np.dot(ray_dir, self.normal)
        if (den == 0): return []
        t = np.dot((self.position - ray_origin), self.normal) / np.dot(ray_dir, self.normal)
        if (t < 0): return []
        return [t]

class aabb (ray_object):
    def __init__(self, box_min:np.ndarray, box_max:np.ndarray, **kwargs) -> None:
        super().__init__()
        self.box_min = np.array(box_min, dtype=np.float32)
        self.box_max = np.array(box_max, dtype=np.float32)

        for key, value in kwargs.items():
            setattr(self, key, value)
    
    # https://tavianator.com/2015/ray_box_nan.html
    # this one is crying for optimization
    def intersect(self, ray_origin: np.ndarray, ray_dir: np.ndarray) -> list:
        tmin, tmax = -np.Infinity, np.Infinity
        
        for i in range(3):
            t1 = (self.box_min[i] - ray_origin[i]) * (np.divide(1, ray_dir[i]))
            t2 = (self.box_max[i] - ray_origin[i]) * (np.divide(1, ray_dir[i]))

            tmin = np.maximum(tmin, np.minimum(t1, t2))
            tmax = np.minimum(tmax, np.maximum(t1, t2))
        
        return [tmin, tmax] if tmax > max(tmin, 0.0) else []

class light:
    def __init__(self, position:np.ndarray, strength:float) -> None:
        self.position = np.array(position, dtype=np.float32)
        self.strength = strength

if __name__ == "__main__":
    b = aabb([-1, -1, -1], [1, 1, 1])
    print(b.intersect([-3, 0, 0], [1, 0, 0]))

