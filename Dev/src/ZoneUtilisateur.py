#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

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
        Widget.__init__(self)

    def on_touch_down(self, touch):
        """
        Define actions to perform when the indicator is touched down
        :param touch: the touch point (position, type of touch, ...)
        """
        global position, rotation
        if touch.is_double_tap and self.collide_point(touch.x, touch.y):
            if self.user.identifier == 1:
                position = self.get_root_window().width / 2, 200
                rotation = 0
            elif self.user.identifier == 2:
                position = self.get_root_window().width - 300, self.get_root_window().height / 2
                rotation = 90
            elif self.user.identifier == 3:
                position = self.get_root_window().width / 2, self.get_root_window().height - 300
                rotation = 180
            elif self.user.identifier == 4:
                position = 200, self.get_root_window().height / 2
                rotation = -90
            clav = Clavier(self.user, self.color, position, rotation)
            self.parent.add_widget(clav)
        if self.collide_point(touch.x, touch.y):
            self.user.validate = True

    def on_touch_up(self, touch):
        """
        Define actions to perform when the indicator is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if self.collide_point(touch.x, touch.y):
            self.user.validate = False
