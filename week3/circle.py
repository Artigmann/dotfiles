#!/usr/bin/env python
"""
Basic circle module.
"""

from math import pi


class Circle:
    """
    Class representing a circle.
    """
    def __init__(self, radius):
        """
        Constructor. Takes the radius of the circle as an argument.
        """
        self.radius = radius

    def area(self):
        """
        Returns the area of the circle.
        """
        return pi*self.radius**2

    def perimeter(self):
        """
        Returns the perimeter (circumference) of the circle.
        """
        return 2*pi*self.radius
