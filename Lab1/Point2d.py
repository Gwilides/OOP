WIDTH = 1000
HEIGHT = 1000

class Point2d:
    __slots__ = ("_x", "_y")

    def __init__(self, x: int, y: int):
        if not (0 <= x <= WIDTH):
            raise ValueError(f"x должен быть в диапазоне от 0 до {WIDTH}")
        if not (0 <= y <= HEIGHT):
            raise ValueError(f"y должен быть в диапазоне от 0 до {HEIGHT}")
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y
    
    def __str__(self):
        return f"({self._x}, {self._y})"
    
    def __repr__(self):
        return f"Point2d({self._x}, {self._y})"
    

if __name__ == "__main__":
    point = Point2d(110, 200)
    point2 = Point2d(100, 200)
    print(point == point2)
    print(point)
    print(repr(point))