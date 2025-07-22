import math

class Vector2D:
    # Initialize a new Vector with an x and y component
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # Returns a new Vector that is the sum of self and other
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    # Returns a new Vector that is the difference of self and other
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    # Returns the dot product of two vectors
    def __mul__(self, other):
        return (self.x * other.x) + (self.y * other.y)
    
    # Checks if two vectors are equal by comparing their respective x and y values
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)
    
    # Returns a scaled vector by multiplying the x and y values by a scalar
    def scale(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    # Returns the magnitude of the vector using cartesian distance
    def mag(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5
    
    # Returns the square of the magnitude of the vector
    def magSQ(self):
        return ((self.x ** 2) + (self.y ** 2))
    
    # Returns a unit vector pointing in the same direction as the original
    def norm(self):
        if self.mag() == 0:
            return Vector(0, 0)
        return self.scale(1 / self.mag())
    
    # Returns a projection of the self onto another vector
    def proj(self, other):
        if other.mag() == 0:
            return Vector(0, 0)
        return other.scale((self * other) / other.magSQ())
    
    # Returns the cartesian distance between two vectors
    def dist(self, other):
        return (other - self).mag()
    
    # Returns the distance between two vectors squared
    def distSQ(self, other):
        return (other - self).magSQ()
    
    # Returns a string representation of the vector in the form (x, y)
    def __str__(self):
        return f"({self.x}, {self.y})"





class Vector:
    # Initialize a new Vector with an x and y component
    def __init__(self, els):
        self.els = els
    
    # Returns a new Vector that is the sum of self and other
    def __add__(self, other):
        if len(self.els) != len(other.els):
            return None
        els = [self.els[i] + other.els[i] for i in range(len(self.els))]
        return Vector(els)
    
    # Returns a new Vector that is the difference of self and other
    def __sub__(self, other):
        if len(self.els) != len(other.els):
            return None
        els = [self.els[i] - other.els[i] for i in range(len(self.els))]
        return Vector(els)
    
    # Returns the dot product of two vectors
    def __mul__(self, other):
        if len(self.els) != len(other.els):
            return None
        els = [self.els[i] * other.els[i] for i in range(len(self.els))]
        return sum(els)
    
    # Checks if two vectors are equal by comparing their respective x and y values
    def __eq__(self, other):
        if len(self.els) != len(other.els):
            return False
        for i in range(len(self.els)):
            if self.els[i] != other.els[i]:
                return False
        return True
    
    # Returns a scaled vector by multiplying the x and y values by a scalar
    def scale(self, scalar):
        return Vector([el * scalar for el in self.els])
    
    # Returns the magnitude of the vector using cartesian distance
    def mag(self):
        return self.magSQ() ** 0.5
    
    # Returns the square of the magnitude of the vector
    def magSQ(self):
        return sum([el ** 2 for el in self.els])
    
    # Returns a unit vector pointing in the same direction as the original
    def norm(self):
        if self.mag() == 0:
            return Vector([0 for _ in self.els])
        return self.scale(1 / self.mag())
    
    # Returns a projection of the self onto another vector
    def proj(self, other):
        if other.mag() == 0:
            return Vector([0 for _ in self.els])
        return other.scale((self * other) / other.magSQ())
    
    # Returns the cartesian distance between two vectors
    def dist(self, other):
        return (other - self).mag()
    
    # Returns the distance between two vectors squared
    def distSQ(self, other):
        return (other - self).magSQ()
    
    # Returns a string representation of the vector in the form (x, y)
    def __str__(self):
        vec = "("
        for el in self.els:
            vec += str(el) + ", "
        return vec[:-2] + ")"
    
    # Returns the x value of the vector or 0 if it doesn't exist
    def x(self):
        if self.els:
            return self.els[0]
        else:
            return 0
    
    # Returns the y value of the vector or 0 if it doesn't exist
    def y(self):
        if len(self.els) >= 2:
            return self.els[1]
        else:
            return 0
    
    # Returns the z value of the vector or 0 if it doesn't exist
    def z(self):
        if len(self.els) >= 2:
            return self.els[2]
        else:
            return 0
    
    # Sets the x value of the vector if it exists
    def setX(self, val):
        if self.els:
            self.els[0] = val
    
    # Sets the y value of the vector if it exists
    def setY(self, val):
        if len(self.els) >= 2:
            self.els[1] = val
    
    # Sets the z value of the vector if it exists
    def setZ(self, val):
        if len(self.els) >= 3:
            self.els[2] = val
    
    # Returns a projection of the vector into 1 dimension lower
    def red(self):
        return Vector([self.els[i] for i in range(len(self.els) - 1)])
    




class Matrix:
    # Creates a new matrix from a list of column vectors
    def __init__(self, cols):
        self.cols = cols
        self.rows = self.getRows()
        self.m = len(self.rows)
        self.n = len(self.cols)
    
    # Generates the rows of a matrix from its column vectors
    def getRows(self):
        return [Vector([col.els[r] for col in self.cols]) for r in range(len(self.cols[0].els))]
    
    # Returns the sum of two matrices
    def __add__(self, other):
        if self.n != other.n or self.m != other.m:
            return None
        cols = [self.cols[c] + other.cols[c] for c in range(len(self.cols))]
        return Matrix(cols)
    
    # Returns the difference between two matrices
    def __sub__(self, other):
        if self.n != other.n or self.m != other.m:
            return None
        cols = [self.cols[c] - other.cols[c] for c in range(len(self.cols))]
        return Matrix(cols)
    
    # Checks whether or not two matrices are equal
    def __eq__(self, other):
        if self.n != other.n or self.m != other.m:
            return False
        cols = [self.cols[c] == other.cols[c] for c in range(len(self.cols))]
        return all(cols)
    
    # Returns the result of multiplying the matrix by the input vector
    def mult(self, vector):
        if len(vector.els) != self.n:
            return None
        return Vector([r * vector for r in self.rows])
        
    # Returns the product of two matrices
    def __mul__(self, other):
        if self.n != other.m:
            return None
        return Matrix([self.mult(c) for c in other.cols])

    # Returns the transpose of the matrix
    def transpose(self):
        return Matrix(self.rows)
    
    # Returns a scaled version of the matrix
    def scale(self, scalar):
        cols = [self.cols[c] * scalar for c in range(len(self.cols))]
        return Matrix(cols)
    
    # Returns a string representation of the matrix
    def __str__(self):
        mat = ""
        for r in self.rows:
            mat += str(r) + '\n'
        return mat
    







class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    @classmethod
    def make(cls, axis, angle):
        return cls(
            w = math.cos(angle / 2),
            x = math.sin(angle / 2) * axis.x(),
            y = math.sin(angle / 2) * axis.y(),
            z = math.sin(angle / 2) * axis.z()
        )
    
    def __mul__(self, other):
        return Quaternion(
            w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
            x = self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y,
            y = self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x,
            z = self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        )
    
    def conjugate(self):
        return Quaternion(
            w = self.w,
            x = -self.x,
            y = -self.y,
            z = -self.z
        )
    
    def normalized(self):
        mag = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        return Quaternion(
            w = self.w / mag,
            x = self.x / mag,
            y = self.y / mag,
            z = self.z / mag
        )
    
    def mult(self, v):
        # Rotate vector v using this quaternion
        q_v = Quaternion(0, v.x(), v.y(), v.z())
        q_conj = self.conjugate()
        q_result = self * q_v * q_conj
        return Vector([q_result.x, q_result.y, q_result.z])
    
    def __str__(self):
        return f"{self.w} + {self.x}i + {self.y}j + {self.z}k"