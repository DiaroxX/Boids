from math import sqrt, atan2

class Vector:
    """
    A helper class to allow for easier manipulation of geometric data in 2D
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)
    
    def magnitude_tore(self, width, height):
        x = min(abs(self.x), abs(width-self.x))
        y = min(abs(self.y), abs(height-self.y))
        return sqrt(x*x + y*y)
    
    def angle(self):
        # atan2 is always between -pi and pi
        return atan2(self.y, self.x)
    
    def __add__(self, other):
        """
        Operator overload to allow for easy vector addition
        """
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise NotImplementedError("Vector can only added to other Vector")
        
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(other * self.x, other * self.y)
        raise NotImplementedError("Vector can only be multiplied by a scalar")
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x / other,  self.y / other)
        raise NotImplementedError("Vector can only be multiplied by a scalar")
 
    def __neg__(self):
        return -1 * self
    
    def __sub__(self, other):
        return self + (-other)
    
    def __repr__(self):
        return f"Vector ({self.x:.1f}, {self.y:.1f})"
    
    def cap_magnitude(self, mag_max):
        self_mag = self.magnitude()
        final_mag = min(self_mag, mag_max)
        self.x *= final_mag / self_mag
        self.y *= final_mag / self_mag
