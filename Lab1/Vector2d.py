from math import sqrt
from Point2d import Point2d

class Vector2d:
    __slots__ = ("_x", "_y")

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @classmethod
    def constructor_from_points(cls, start: Point2d, end: Point2d):
        return cls(end.x - start.x, end.y - start.y)
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
    def __getitem__(self, index):
        return getattr(self, self.__slots__[index])

    def __setitem__(self, index, value):
        setattr(self, self.__slots__[index], value)

    def __iter__(self):
        yield self._x
        yield self._y

    def __len__(self):
        return 2
    
    def __eq__(self, other):
        return self._x == other._x and self._y == other._y
    
    def __str__(self):
        return f"({self._x}, {self._y})"
    
    def __repr__(self):
        return f"Vector2d({self._x}, {self._y})"
    
    def __abs__(self):
        return sqrt(self._x**2 + self._y**2)
    
    def __add__(self, other):
        return Vector2d(self._x + other.x, self._y + other.y)
    
    def __sub__(self, other):
        return Vector2d(self._x - other.x, self._y - other.y)
    
    def __mul__(self, number):
        return Vector2d(self._x * number, self._y * number)
    
    def __truediv__(self, number):
        if (number == 0):
            raise ZeroDivisionError("Деление на ноль")
        return Vector2d(self._x / number, self._y / number)
        
    def dot(self, vector):
        return self._x * vector.x + self._y * vector.y
    
    def cross(self, vector):
        return self._x * vector.y - self._y * vector.x

    @classmethod
    def dot_cls(cls, vector1, vector2):
        return vector1.dot(vector2)
    
    @classmethod
    def cross_cls(cls, vector1, vector2):
        return vector1.cross(vector2)
    
    @staticmethod
    def triple_product(vector1, vector2, vector3):
        return 0
    
if __name__ == "__main__":
    v1 = Vector2d(2, 3)
    v2 = Vector2d(3, 4)
    print("v1 == v2:", v1 == v2)
    print(v1[0])
    print(v1)
    print(repr(v1))
    print(abs(v2))
    v3 = v1 + v2
    print(v3)
    v4 = v2 - v1
    print(v4)
    v5 = v1 * 2
    print(v5)
    v6 = v1 / 2
    print(v6)
    print(v1.dot(v2))
    print(v1.cross(v2))
    print(Vector2d.dot_cls(v1, v2))
    print(Vector2d.cross_cls(v1, v2))
    start = Point2d(1, 1)
    end = Point2d(4, 5)
    v7 = Vector2d.constructor_from_points(start, end)
    print(v7)
    for i in v1:
        print(i)