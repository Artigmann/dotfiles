#!/usr/bin/env python
"""
Basic circle module with attributes and properties. We
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
        self.radius = radius

    def set_radius(self, radius):
        """
        Sets radius of circle. Radius needs to be a positive number.
        """
        if radius > 0:
            self.__radius = radius
        else:
            raise ValueError("Radius needs to be positive.")

    def get_radius(self):
        """
        Returns radius.
        """
        return self.__radius

    def set_area(self, area):
        """
        Sets radius of circle based on area. Area needs to be a positive number.
        """
        if area > 0:
            self.__radius = sqrt(area/pi)
        else:
            raise ValueError("Area needs to be positive.")

    def get_area(self):
        """
        Returns area.
        """
        return pi*self.__radius**2

    def set_perimeter(self, perimeter):
        """
        Sets radius of circle based on perimeter. Perimeter needs to be a positive number.
        """
        if perimeter > 0:
            self.__radius = perimeter/(2*pi)
        else:
            raise ValueError("Perimeter needs to be positive.")

    def get_perimeter(self):
        """
        Returns perimeter.
        """
        return 2*self.__radius*pi

    radius = property(fget=get_radius, fset=set_radius)
    area = property(fget=get_area, fset=set_area)
    perimeter = property(fget=get_perimeter, fset=set_perimeter)
