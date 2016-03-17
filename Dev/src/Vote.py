from math import pi, sin, cos

from kivy.graphics import Ellipse
from kivy.uix.colorpicker import Color
from kivy.uix.widget import Widget


class Vote(Widget):
    """
    A class to represent the indicator of the user's zone
    """
    def __init__(self, id_usr, value, pos, angle):
        """

        :return:
        """
        self.value = value
        self.id_usr = id_usr
        self.angle = angle
        self.size = (50,50)
        move_x = 0
        move_y = 0
        if self.angle == 270:
            move_y = -50
        elif self.angle == 180:
            move_x = -50
            move_y = -50
        elif self.angle == 90:
            move_x = -50

        self.angle = float(self.angle)/180.*pi
        if self.value == 1:
            self.Position = pos[0]+(150*cos(self.angle))+move_x, pos[1]+(150*sin(self.angle))+move_y
        else:
            self.Position = pos[0]+(200*cos(self.angle))+move_x, pos[1]+(200*sin(self.angle))+move_y
        self.pos = self.Position
        Widget.__init__(self)
        print self.pos
        with self.canvas:
            if self.value == 0:
                Color(1,0,0,1)
            else:
                Color(0,1,0,1)
            Ellipse(pos=self.pos,size=self.size)

    def on_touch_move(self, touch):
        if self.collide_point(touch.x,touch.y):
            self.canvas.clear()
            self.pos = touch.x-25,touch.y-25
            with self.canvas:
                if self.value == 0:
                    Color(1,0,0,1)
                else:
                    Color(0,1,0,1)
                Ellipse(pos=self.pos,size=self.size)
            for criterion in self.parent.parent.criterions:
                if self.collide_widget(criterion):
                    criterion.validate_by_user(self.id_usr, self.value)
                    self.canvas.clear()
                    self.pos = self.Position
                    with self.canvas:
                        if self.value == 0:
                            Color(1,0,0,1)
                        else:
                            Color(0,1,0,1)
                        Ellipse(pos=self.pos,size=self.size)

    def on_touch_up(self, touch):
        if self.collide_point(touch.x,touch.y):
            self.canvas.clear()
            self.pos = self.Position
            with self.canvas:
                if self.value == 0:
                    Color(1,0,0,1)
                else:
                    Color(0,1,0,1)
                Ellipse(pos=self.pos,size=self.size)