#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from math import cos, sin

from kivy.uix.image import Image
from kivy.uix.scatter import Scatter


class Vote(Scatter):
    """
    A class to represent vote token
    """

    def __init__(self, id_usr, value, pos, angle, user):
        """
        Initialize the vote token
        """
        self.value = value
        self.id_usr = id_usr
        self.angle = angle
        self.size = (50, 50)
        self.vote = []
        self.user = user
        self.do_rotation = False
        self.do_scale = False

        if self.value == 0:
            self.texture = Image(source="Images/unvalidate.png").texture
            self.color = (self.user.color[0] / 2, self.user.color[1] / 2, self.user.color[2] / 2, 1)
        else:
            if angle == 180 :
                self.texture = Image(source="Images/validate180.png").texture
            elif angle == 0:
                self.texture = Image(source="Images/validate.png").texture
            else :
                self.texture = Image(source="Images/validate90.png").texture
            self.color = (3 * self.user.color[0] / 4, 3 * self.user.color[1] / 4, 3 * self.user.color[2] / 4, 1)

        move_x = +125
        move_y = 0

        if self.angle == 180:
            move_x = -175
            move_y = -50

        if self.angle == 90:
            move_x= 0
            move_y= -180

        if self.value == 0:
            self.Position = (pos[0]+move_x,pos[1]+move_y)
        else:
            if self.angle == 180:
                self.Position = (pos[0] + (move_x - 300) * cos(self.angle) - 160, pos[1] + move_y)
            elif self.angle == 0:
                self.Position = (pos[0]+(move_x - 300)*cos(self.angle),pos[1]+move_y)
            else :
                self.Position = (pos[0]+move_x,pos[1]+(move_y-105)*cos(self.angle))
        Scatter.__init__(self)
        self.pos = self.Position


    def on_touch_up(self, touch):
        """
        Define actions to perform when the token is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if self.collide_point(touch.x, touch.y):
            for criterion in self.parent.parent.criterions:
                if self.collide_point(criterion.center[0], criterion.center[1]) and not self.collide_widget(
                        self.parent.parent.get_zone_utilisateur(self.user)):
                    criterion.validate_by_user(self.id_usr, self.value)
                    self.parent.parent.update_vote()
            self.pos = self.Position

        Scatter.on_touch_up(self, touch)