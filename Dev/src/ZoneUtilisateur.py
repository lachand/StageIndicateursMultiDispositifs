#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from Clavier import Clavier


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
        self.ti_pos = 0,0
        self.angle = 0
        self.has_text_input = False
        Widget.__init__(self)

    def set_name(self, name):
        """
        Set the name of the thone
        :param name: new name of the zone
        """
        if self.name is not None:
            self.remove_widget(self.name)
        print "ajout du nom :" + name
        if self.user.identifier == 1:
            self.name = Label(text=name)
            self.name.pos=(self.position[0]+self.name.size[0],0)
            self.angle = 0
            self.ti_pos = self.name.pos=(self.position[0]+200,0)
        elif self.user.identifier == 2:
            self.name = Label(text=name)
            self.name.pos = (self.position[0]+self.name.size[0],self.parent.height -100)
            self.angle = 90
            self.ti_pos = self.name.pos = (self.position[0]+200,self.parent.height -100)
        elif self.user.identifier == 3:
            self.name = Label(text=name)
            self.name.pos = (self.position[0] + self.name.size[0], self.parent.height - 100)
            self.angle = 180
            self.ti_pos = (self.position[0] + 200, self.parent.height - 100)
        elif self.user.identifier == 4:
            self.name = Label(text=name)
            self.name.pos = (self.position[0] + self.name.size[0], 0)

        self.user.name = name
        self.connected = True
        self.add_widget(self.name)

    def is_connected(self):
        """
        Return if the user is connected or not
        :return: if the user is connected or not
        """
        return self.connected

    def on_touch_down(self, touch):
        """
        Define actions to perform when the indicator is touched down
        :param touch: the touch point (position, type of touch, ...)
        """
        if touch.is_double_tap and self.collide_point(touch.x, touch.y) and not self.has_text_input:
            clavier = Clavier(self.user, self.color, self.ti_pos, self.angle, "table")
            self.parent.add_widget(clavier)
            clavier.initialisation()
            self.has_text_input = True
        else:
            if self.collide_point(touch.x, touch.y):
                self.user.validate = True
        Widget.on_touch_down(self,touch)

    def on_touch_up(self, touch):
        """
        Define actions to perform when the indicator is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if self.collide_point(touch.x, touch.y):
            self.user.validate = False
        Widget.on_touch_up(self,touch)

    def initialisation(self):
        if self.user.identifier == 1:
            self.angle = 0
            self.ti_pos=(self.position[0]+100,200)
        elif self.user.identifier == 2:
            self.angle = 180
            self.ti_pos =(self.position[0]+100,self.parent.height - 300)
        elif self.user.identifier == 3:
            self.angle = -90
            self.ti_pos = (self.position[0] + 400, self.parent.height - 450)