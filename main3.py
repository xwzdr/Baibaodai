import math


# Базовый класс
class Figure:
    def area(self):
        raise NotImplementedError("Этот метод должен быть переопределен.")

    def perimeter(self):
        raise NotImplementedError("Этот метод должен быть переопределен.")

    def compare_area(self, other):
        raise NotImplementedError("Этот метод должен быть переопределен.")

    def compare_perimeter(self, other):
        raise NotImplementedError("Этот метод должен быть переопределен.")


# Квадрат
class Square(Figure):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side

    def compare_area(self, other):
        return self.area() > other.area()

    def compare_perimeter(self, other):
        return self.perimeter() > other.perimeter()


# Прямоугольник
class Rectangle(Figure):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def compare_area(self, other):
        return self.area() > other.area()

    def compare_perimeter(self, other):
        return self.perimeter() > other.perimeter()


# Треугольник
class Triangle(Figure):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def perimeter(self):
        return self.base + self.base + math.sqrt(self.base ** 2 + self.height ** 2)

    def compare_area(self, other):
        return self.area() > other.area()

    def compare_perimeter(self, other):
        return self.perimeter() > other.perimeter()


# Круг
class Circle(Figure):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

    def compare_area(self, other):
        return self.area() > other.area()

    def compare_perimeter(self, other):
        return self.perimeter() > other.perimeter()


# Примерение
square = Square(5)
rectangle = Rectangle(4, 6)
triangle = Triangle(3, 4)
circle = Circle(7)

print("Площади квадрата:", square.area())
print("Периметр	prямоугольника:", rectangle.perimeter())
print("Площади треугольника:", triangle.area())
print("Перимет круга:", circle.perimeter())

# Сравнение площади и периметра
print("Квадрат vs Круг площади:", square.compare_area(circle))
print("Прямоугольник vs Треугольник периметра:", rectangle.compare_perimeter(triangle))