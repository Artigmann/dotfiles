#!/usr/bin/env python
"""
Basic circle module with several attributes using properties. We allow negative
and zero radius. Area and circumference needs to be zero or higher. We use
instance checking of numbers given as argument, even though it's perhaps
less pythonesque.

Should check if what values are reasonable for radius.
"""

from numbers import Number
from math import pi, sqrt


class FlexCircle(object):
    """
    Circle class using attributes and properties.
    """
    def __init__(self, radius):
        """
        Constructor, takes a radius as a Number or raises a ValueError if not
        a number.
        """
        if isinstance(radius, Number):
            self.__radius = radius
        else:
            raise ValueError("Radius needs to be a number")

    def set_radius(self, radius):
        """
        Sets radius with given number or throws ValueError if not a number.
        """
        if isinstance(radius, Number):
            self.__radius = radius
        else:
            raise ValueError("Radius needs to be a number")

    def get_radius(self):
        """
        Returns radius.
        """
        return self.__radius

    def set_area(self, area):
        """
        Sets area with given zero or higher number or throws ValueError if area
        fails to conform to this.
        """
        if isinstance(area, Number) and area >= 0:
            self.__radius = sqrt(area/pi)
        else:
            raise ValueError("Area needs to be a number that is 0 or higher")

    def get_area(self):
        """
        Returns area.
        """
        return pi*self.__radius**2

    def set_perimeter(self, perimeter):
        """
        Sets perimeter given argument, argument has to be a number that is 0 or
        higher or ValueError is raised.
        """
        if isinstance(perimeter, Number) and perimeter >= 0:
            self.__radius = perimeter/(2*pi)
        else:
            raise ValueError("Perimeter needs to be a number that is 0 or " +
                             "higher")

    def get_perimeter(self):
        """
        Returns perimeter.
        """
        return 2*self.__radius*pi

    radius = property(fget=get_radius, fset=set_radius)
    area = property(fget=get_area, fset=set_area)
    perimeter = property(fget=get_perimeter, fset=set_perimeter)
