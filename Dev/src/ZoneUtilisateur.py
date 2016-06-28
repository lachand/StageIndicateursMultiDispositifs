#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.uix.label import Label
from kivy.uix.widget import Widget


class ZoneUtilisateur(Widget):
    """
    A class to represent the indicator of the user's zone
    """
    def __init__(self, user, pos):
        """
        Initialize the indicator
        :param user: the user of which the indicator is about
        :param pos: the position of the indicator
        """
        self.user = user
        self.size = [300, 300]
        self.position = pos[0] - self.size[0] / 2, pos[1] - self.size[1] / 2
        self.color = self.user.color
        self.connected = False
        self.name = None
        Widget.__init__(self)

    def set_name(self, name):
        if self.name is not None:
            self.remove_widget(self.name)
        print "ajout du nom :" + name
        if self.user.identifier == 1:
            self.name = Label(text=name)
            self.name.pos=(self.position[0]+self.name.size[0],0)
        elif self.user.identifier == 2:
            self.name = Label(text=name)
            self.name.pos = (self.position[0]+self.name.size[0],self.parent.height -100)
        elif self.user.identifier == 3:
            self.name = Label(text=name)
            self.name.pos = (self.position[0] + self.name.size[0], self.parent.height - 100)
        elif self.user.identifier == 4:
            self.name = Label(text=name)
            self.name.pos = (self.position[0] + self.name.size[0], 0)

        self.user.name = name
        self.connected = True
        self.add_widget(self.name)

    def is_connected(self):
        return self.connected

    def on_touch_down(self, touch):
        """
        Define actions to perform when the indicator is touched down
        :param touch: the touch point (position, type of touch, ...)
        """
        if self.collide_point(touch.x, touch.y):
            self.user.validate = True

    def on_touch_up(self, touch):
        """
        Define actions to perform when the indicator is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if self.collide_point(touch.x, touch.y):
            self.user.validate = False
