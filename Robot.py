# -*- coding=utf-8 -*-

import warnings


class BaseRobot:
    def __init__(self):
        self.location = (0, 0)  # A robot always starts at the origin
        self._orientation = 0  # For the orientation property
    
    def move(self, x, y):
        """
        :param int x: number of unit the robot should move in the coordinate plane on x-axis
        :param int y: number of unit the robot should move in the coordinate plane on y-axis
        :return: coordinate after moving
        """
        
        raise NotImplemented
    
    @property
    def orientation(self):
        "The orientation of the robot is calculated in degrees, from -179 to 180, relative to the x-axis of the coordinate plane, as in a unit circle"
        return self._orientation
    
    @orientation.setter
    def orientation(self, value):
        try:
            assert (value <= 360), "Orientation should be smaller than 360 degree"
            assert (value >= - 180), "Orientation should be greater than -180 degree"
        except AssertionError as err:
            err = ValueError(err)
            err.__suppress_context__ = True
            raise err
        if - 6.29 < value < 6.29:
            warnings.warn("Orientation angle %f is too small. Check if it is converted to degrees." % value)
        
        if value > 180: value -= 360
        
        self._orientation = int(value)
    
    def turn(self, degree):
        """
        :param int degree: degree the robot should turn
        :return: coordinate after turning
        """
        raise NotImplemented
    
    def is_moving(self):
        """
        :return: boolean, whether the robot is moving or not
        """
        
        raise NotImplemented
    
    def calculate_location(self, angle_turned, distance_traveled, last_node):
        raise NotImplemented
