#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from math import sin, cos, pi
from random import randint

from kivy.graphics import Rectangle
from kivy.uix.colorpicker import Color
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from shapely.geometry import Polygon

from ZoneUtilisateur import ZoneUtilisateur


class Animal(Scatter):
    """
    A Class representing an animal
    """
    def __init__(self, identifier, image, pos):
        """
        Initialize an animal
        :param identifier: the id of the animal
        :param image: the path of the image for the animal
        :param pos: the square where the scater can be randomly placed
        """
        self.color = [0, 0, 0]
        Scatter.__init__(self)
        self.src_image = image
        self.image = Image(source=image)
        self.size = self.image.size
        self.center = [randint(200, pos[0]), randint(200, pos[1])]
        self.identifier = identifier
        self.current_user = None
        self.on_move = False
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(source=self.src_image, size=[self.size[0] - 10, self.size[1] - 10])

    def set_user(self, user):
        """
        Set the current user of the animal
        :param user: the user that is using the animal
        """
        self.current_user = user
        self.color = user.color
        self.canvas.clear()
        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2])
            Rectangle()
            Color(1, 1, 1, 1)
            Rectangle(source=self.src_image, size=[self.size[0] - 10, self.size[1] - 10])

    def remove_user(self):
        """
        Remove the current user of the animal
        """
        self.current_user = None
        self.color = [1, 1, 1]
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(source=self.src_image, size=[self.size[0] - 10, self.size[1] - 10])

    def on_touch_move(self, touch):
        """
        Update the distance and angle between the animal and each of his links and set the user touching the animal
        :param touch: the position of the touch
        """
        if self.collide_point(touch.x, touch.y):
            for criterion in self.parent.criterions:
                value = criterion.has_link(self.identifier)
                if value != -1:
                    criterion.update_link(value, self.center)

            for child in self.parent.children:
                if child.__class__ == ZoneUtilisateur and child.collide_point(self.center[0], self.center[1]):
                    if self.current_user is None:
                        self.set_user(child.user)
            Scatter.on_touch_move(self, touch)

    def update_coordinate(self, x, y):
        """
        Update the coordinate of the Animal considering his links
        :param x: the new x coordinate
        :param y: the new y coordinate
        """
        points = []
        for criterion in self.parent.criterions:
            for link in criterion.links:
                if link.linked_to_animal(self.identifier):
                    x = criterion.center_x + link.distance*cos(link.angle+pi)
                    y = criterion.center_y + link.distance*sin(-link.angle+pi)
                    points.append([x, y])
        if len(points) == 1:
            if 0 < x < self.parent.size[0]:
                self.center_x = x
            if 0 < y < self.parent.size[1]:
                self.center_y = y
        elif len(points) == 2:
            x = (points[0][0] + points[1][0])/2
            y = (points[0][1] + points[1][1])/2
            if 0 < x < self.parent.size[0]:
                self.center_x = x
            if 0 < y < self.parent.size[1]:
                self.center_y = y
        elif len(points) > 2:
            poly = Polygon(points)
            point = poly.centroid
            if 0 < x < self.parent.size[0]:
                self.center_x = point.x
            if 0 < y < self.parent.size[1]:
                self.center_y = point.y
