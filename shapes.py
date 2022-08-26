import math

def print_message(msg, end=False):
    if not end: 
        print()
    print('=' * 50)
    print(msg)
    print('=' * 50)


class Point:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
    def __repr__(self):           # __repr__ means represent (2 underscores before/after)
        return f'({self.x},{self.y})'
    def move_to(self, x, y): 
        self.x, self.y = x, y
    def move_by(self, deltax, deltay):
        self.x += deltax
        self.y += deltay
    @staticmethod
    def run_tests():
        print_message('RUNNING TESTS on class POINT')

        pt = Point()
        print(f'pt is {pt}')
        pt.move_to(x=10, y=20)
        print(f'pt has been moved to {pt}')
        pt.move_by(deltax=1, deltay=1)
        print(f'pt has been moved by (1, 1) to {pt}')

        pt2 = Point(x=3, y=-3)
        print(f'pt2 is {pt2}')
        pt2.move_to(x=1, y=2)
        print(f'pt2 has been moved to {pt2}')
        pt2.move_by(deltax=3, deltay=-3)
        print(f'pt2 has been moved by (3, -3) to {pt2}')

        print_message('ENDING TESTS on class POINT', end=True)


class Circle:
    def __init__(self, radius=0, center=Point()):
        self.radius = radius
        self.center = center
    # stroke color    # still TODO -- needs graphics mode
    # fill color      # still TODO -- needs graphics mode

    def __repr__(self):
        return f'Circle(r={self.radius},area={self.area():.2f},circum={self.circumference():.2f},center={self.center})'

    def diameter(self): return 2 * self.radius
    def area(self): return math.pi * self.radius ** 2
    def perimeter(self): return self.circumference()
    def circumference(self): return 2 * math.pi * self.radius 

    def inflate(self, deltar): self.radius += deltar
    def set_radius(self, radius): self.radius = radius
    def move_to(self, x, y): self.center.move_to(x, y)
    def move_by(self, deltax, deltay): self.center.move_by(deltax, deltay) 
    @staticmethod
    def run_tests():
        print_message('RUNNING TESTS on class POINT')

        c = Circle(radius=5, center=Point())
        print(c)
        c.move_to(x=10, y=20)
        print(f'c has been moved to {c}')
        c.move_by(deltax=1, deltay=1)
        print(f'c has been moved by (1, 1) to {c}')

        c2 = Circle(radius=10, center=Point(3, 5))
        print(c2)
        c2.move_to(x=10, y=20)
        print(f'c2 has been moved to {c2}')
        c2.move_by(deltax=1, deltay=1)
        print(f'c2 has been moved by (1, 1) to {c2}')

        print_message('ENDING TESTS on class CIRCLE', end=True)


def main():
    Circle.run_tests()
    Point.run_tests()
    print()
    

if __name__ == '__main__':
    main()


# ==================================================
# OUTPUT
# ==================================================

# ==================================================
# RUNNING TESTS on class POINT
# ==================================================
# Circle(r=5,area=78.54,circum=31.42,center=(0,0))
# c has been moved to Circle(r=5,area=78.54,circum=31.42,center=(10,20))
# c has been moved by (1, 1) to Circle(r=5,area=78.54,circum=31.42,center=(11,21))
# Circle(r=10,area=314.16,circum=62.83,center=(3,5))
# c2 has been moved to Circle(r=10,area=314.16,circum=62.83,center=(10,20))
# c2 has been moved by (1, 1) to Circle(r=10,area=314.16,circum=62.83,center=(11,21))
# ==================================================
# ENDING TESTS on class CIRCLE
# ==================================================

# ==================================================
# RUNNING TESTS on class POINT
# ==================================================
# pt is (0,0)
# pt has been moved to (10,20)
# pt has been moved by (1, 1) to (11,21)
# pt2 is (3,-3)
# pt2 has been moved to (1,2)
# pt2 has been moved by (3, -3) to (4,-1)
# ==================================================
# ENDING TESTS on class POINT
# ==================================================
