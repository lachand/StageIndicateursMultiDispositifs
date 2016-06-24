#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.graphics import Rectangle
from kivy.uix.colorpicker import Color
from kivy.uix.image import Image
from kivy.uix.widget import Widget


class Vote(Widget):
    """
    A class to represent the indicator of the user's zone
    """

    def __init__(self, id_usr, value, pos, angle, user):
        """
        Initialize the vote
        """
        self.value = value
        self.id_usr = id_usr
        self.angle = angle
        self.size = (50, 50)
        self.vote = []
        self.user = user
        if angle == 180:
            yes = Image(source="Images/validate180.png")
        else:
            yes = Image(source="Images/validate.png")
        no = Image(source="Images/unvalidate.png")
        self.texture_yes = yes.texture
        self.texture_no = no.texture
        self.do_scale = False
        self.do_rotation = False
        self.rotation = self.angle
        move_x = +50
        move_y = 0
        if self.angle == 180:
            move_x = -100
            move_y = -50

        self.Position = (pos[0]+move_x,pos[1]+move_y)
        Widget.__init__(self)
        with self.canvas:
            if self.value == 0:
                Color(self.user.color[0] / 2, self.user.color[1] / 2, self.user.color[2] / 2, 1)
                self.pos = self.Position
                Rectangle(pos=self.pos, size=self.size, texture=self.texture_no, color=(self.user.color[0],self.user.color[1],self.user.color[2],.25))
            else:
                Color(3 * self.user.color[0] / 4, 3 * self.user.color[1] / 4, 3 * self.user.color[2] / 4, 1)
                if self.angle == 0:
                    self.Position = self.Position[0] - 150, self.Position[1]
                elif self.angle == 180:
                    self.Position = self.Position[0] + 100, self.Position[1]
                self.pos = self.Position
                if self.value == 1:
                    Rectangle(pos=self.pos, size=self.size, texture=self.texture_yes)
                else:
                    Rectangle(pos=self.pos, size=self.size, texture=self.texture_no)


    def on_touch_move(self, touch):
        """
        Define actions to perform when the indicator is moved
        :param touch: the touch point (position, type of touch, ...)
        """
        if self.collide_point(touch.x, touch.y):
            self.canvas.clear()
            self.pos = touch.x - 25, touch.y - 25
            with self.canvas:
                if self.value == 0:
                    Color(self.user.color[0] / 2, self.user.color[1] / 2, self.user.color[2] / 3, 1)
                else:
                    Color(3 * self.user.color[0] / 4, 3 * self.user.color[1] / 4, 3 * self.user.color[2] / 4, 1)
                if self.value == 1:
                    Rectangle(pos=self.pos, size=self.size, texture=self.texture_yes)
                else:
                    Rectangle(pos=self.pos, size=self.size, texture=self.texture_no)
            for criterion in self.parent.parent.criterions:
                if self.collide_point(criterion.center[0], criterion.center[1]) and not self.collide_widget(self.parent.parent.get_zone_utilisateur(self.user)):
                    criterion.validate_by_user(self.id_usr, self.value)
                    self.parent.parent.update_vote()
                    self.canvas.clear()
                    self.pos = self.Position
                    with self.canvas:
                        if self.value == 0:
                            Color(self.user.color[0] / 2, self.user.color[1] / 2, self.user.color[2] / 2, 1)
                        else:
                            Color(3 * self.user.color[0] / 4, 3 * self.user.color[1] / 4, 3 * self.user.color[2] / 4, 1)
                        if self.value == 1:
                            Rectangle(pos=self.pos, size=self.size, texture=self.texture_yes)
                        else:
                            Rectangle(pos=self.pos, size=self.size, texture=self.texture_no)

    def on_touch_up(self, touch):
        """
        Define actions to perform when the indicator is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if self.collide_point(touch.x, touch.y):
            self.canvas.clear()
            self.pos = self.Position
            with self.canvas:
                if self.value == 0:
                    Color(self.user.color[0] / 4, self.user.color[1] / 4, self.user.color[2] / 4, 1)
                else:
                    Color(self.user.color[0] / 2, self.user.color[1] / 2, self.user.color[2] / 2, 1)
                if self.value == 1:
                    Rectangle(pos=self.pos, size=self.size, texture=self.texture_yes)
                else:
                    Rectangle(pos=self.pos, size=self.size, texture=self.texture_no)