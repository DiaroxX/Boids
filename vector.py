from math import sqrt, atan2, pi, cos, sin

def value_with_min_abs(a, b):
    if abs(a) < abs(b):
        return a
    return b

def angle_diff(a, b):
    diff = a-b
    return (diff+pi) % (2*pi) - pi

class Vector:
    """
    A helper class to allow for easier manipulation of geometric data in 2D
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance_tore(self, other, width, height):
        d = self.distance_normale(other)
        x1 = d.x
        x2 = width - x1
        y1 = d.y
        y2 = height - y1
        return Vector(value_with_min_abs(x1, x2), value_with_min_abs(y1, y2))
    
    def distance_normale(self, other):
        return other - self
    
    def distance(self, other, width, height, isTore=True):
        if isTore:
            return self.distance_tore(other, width, height)
        return self.distance_normale(other)

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)
    
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
    
    def cap_angle_diff(self, self_before, max_ang_diff=pi/8):
        mag = self.magnitude()
        curr_ang = self.angle()
        ang_before = self_before.angle()
        new_ang = curr_ang

        ang_diff = angle_diff(curr_ang, ang_before)

        if ang_diff > max_ang_diff:
            new_ang = ang_before + max_ang_diff
        elif -ang_diff > max_ang_diff:
            new_ang = ang_before - max_ang_diff

        self.x = cos(new_ang) * mag
        self.y = sin(new_ang) * mag