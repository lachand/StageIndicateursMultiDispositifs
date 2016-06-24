#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from math import sin, cos, pi
from random import randint

from kivy.graphics import Rectangle
from kivy.uix.colorpicker import Color
from kivy.uix.scatter import Scatter

from ZoneUtilisateur import ZoneUtilisateur


class Animal(Scatter):
    """
    A Class representing an animal
    """

    def __init__(self, identifier, image, pos, parent, support, lvl):
        """
        Initialize an animal
        :param identifier: the id of the animal
        :param image: the path of the image for the animal
        :param pos: the square where the scatter can be randomly placed
        """
        self.support = support
        self.color = [0, 0, 0]
        self.scale_min=1
        self.scale_max=3.
        Scatter.__init__(self)
        self.src_image = image
        if self.support == "table":
            self.center = [randint(200, pos[0]), randint(200, pos[1])]
        else:
            self.center = pos[0], pos[1]
        self.rotation = randint(0,360)
        self.identifier = identifier
        self.current_user = None
        self.on_move = False
        with self.canvas:
            if self.src_image is not None:
                from kivy.uix.image import Image
                from kivy.loader import Loader
                proxy_image = Loader.image(str(self.src_image))
                proxy_image.bind(on_load=self._image_loaded)
                self.image = Image()
        self.locked = False
        self.lvl = lvl


    def _image_loaded(self, proxy_image):
        """
        Load the image from educatouch

        :param proxy_image: The adress of the image to load
        """
        if proxy_image.image.texture:
            self.image.texture = proxy_image.image.texture
            self.image.opacity = 0
            with self.canvas:
                Rectangle(texture=self.image.texture, size=self.image.size)

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
            Rectangle(texture=self.image.texture, size=[self.size[0] - 10, self.size[1] - 10])

    def remove_user(self):
        """
        Remove the current user of the animal
        """
        self.current_user = None
        self.color = [1, 1, 1]
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(texture=self.image.texture, size=[self.size[0] - 10, self.size[1] - 10])

    def on_touch_move(self, touch):
        """
        Update the distance and angle between the animal and each of his links and set the user touching the animal
        :param touch: the position of the touch
        """
        from main import Tablette
        if self.parent is not None:
            for criterion in self.parent.criterions:
                value = criterion.has_link(self.identifier)
                if value != -1:
                    criterion.update_link(value, self.center)
        if self.parent.__class__.__name__ == Tablette.__name__:
            if touch.y > self.parent.height - 40:
                self.parent.client.send_msg('{"Animal" : "' + str(self.identifier) + '"}')
                self.parent.remove_animal(self)
                self.canvas.clear()
        Scatter.on_touch_move(self, touch)

    def on_touch_up(self, touch):
        """
        Action to perform when an user release the animal
        :param touch:
        """
        Scatter.on_touch_up(self, touch)
        if self.collide_point(touch.x, touch.y) and self.parent is not None:
            for child in self.parent.children:
                if child.__class__ == ZoneUtilisateur and child.collide_point(self.center[0], self.center[1]):
                    if self.current_user is None or self.current_user.identifier != child.user.identifier:
                        self.parent.server.send_msg(
                            '{"Image" : "' + str(self.src_image) + '", "ID" : "' + str(self.identifier) + '"}\n',
                            child.user.socket)
                        self.set_user(child.user)

    def update_coordinate(self, x, y):
        """
        Update the coordinate of the Animal considering his links
        :param x: the new x coordinate
        :param y: the new y coordinate
        """
        points = []
        list_x = []
        list_y = []
        for criterion in self.parent.criterions:
            for link in criterion.links:
                if link.linked_to_animal(self.identifier) and not criterion.fused:
                    x = criterion.center_x + link.distance * cos(link.angle + pi)
                    y = criterion.center_y + link.distance * sin(-link.angle + pi)
                    points.append([x, y])
                    list_x.append(x)
                    list_y.append(y)
        if len(points) == 1:
            if 0 < x < self.parent.size[0]:
                self.center_x = x
            if 0 < y < self.parent.size[1]:
                self.center_y = y
        elif len(points) == 2:
            x = (points[0][0] + points[1][0]) / 2
            y = (points[0][1] + points[1][1]) / 2
            if 0 < x < self.parent.size[0]:
                self.center_x = x
            if 0 < y < self.parent.size[1]:
                self.center_y = y
        elif len(points) > 2:
            try:
                point = (sum(x[0]) / len(x[0]), sum(y[1]) / len(y[1]))
                if 0 < x < self.parent.size[0]:
                    self.center_x = point.x
                if 0 < y < self.parent.size[1]:
                    self.center_y = point.y
            except TypeError:
                pass
