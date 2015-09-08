#!/usr/bin/env python
"""
Basic circle module. We allow negative and zero radius. Area and circumference
needs to be zero or higher.
"""

from numbers import Number
from math import pi, sqrt


class FlexCircle(object):
    def __init__(self, radius):
        if isinstance(radius, Number):
            self.__radius = radius
        else:
            raise ValueError("Radius needs to be a number")

    def set_radius(self, radius):
        if isinstance(radius, Number):
            self.__radius = radius
        else:
            raise ValueError("Radius needs to be a number")

    def get_radius(self):
        return self.__radius

    def set_area(self, area):
        if isinstance(area, Number) and area >= 0:
            self.__radius = sqrt(area/pi)
        else:
            raise ValueError("Area needs to be a number that is 0 or higher")

    def get_area(self):
        return pi*self.__radius**2

    def set_perimeter(self, perimeter):
        if isinstance(perimeter, Number) and perimeter >= 0:
            self.__radius = perimeter/(2*pi)
        else:
            raise ValueError("Perimeter needs to be a number that is 0 or " +
                             "higher")

    def get_perimeter(self):
        return 2*self.__radius*pi

    radius = property(fget=get_radius, fset=set_radius)
    area = property(fget=get_area, fset=set_area)
    perimeter = property(fget=get_perimeter, fset=set_perimeter)
