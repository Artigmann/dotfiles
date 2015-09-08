#!/usr/bin/env python
"""
Very basic string handling.
"""


class SimpleString:
    """
    Very basic string handling class.
    """
    def getString(self):
        """
        Takes a string from keyboard input and stores it in the instance.
        """
        print "Enter String value:",
        self.string = raw_input()

    def printString(self):
        """
        Prints string stored in instance in upper case.
        """
        if hasattr(self, 'string'):
            print self.string.upper()
