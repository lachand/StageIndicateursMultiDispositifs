#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput

from Critere import Critere
from PhysicalIndicator import PhysicalIndicator


class Clavier(Scatter):
    """
    A class representing a keyboard for criterion creation
    """
    def __init__(self, user, color, position, angle):
        """
        Initialize the keyboard
        :param user: the user which is creating the criterion
        :param color: the color of the user
        :param position: the position of the keyboard
        :param angle: the angle of the keyboard
        """
        Scatter.__init__(self)
        self.user = user
        self.identifier = self.user.identifier
        self.color = color
        self.pos = position
        self.rotation = angle
        self.ti = TextInput(size_hint=(None, None), multiline=False, size=(100, 30))
        self.ti.bind(on_text_validate=self.validate)
        self.ti.bind(on_double_tap=self.destroy)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False
        self.add_widget(self.ti)
        self.ti.background_color = self.color+[1]
        self.ti.foreground_color = [1, 1, 1, 1]

    def destroy(self, value):
        """
        Destroy the keyboard
        """
        self.ti.focus = False
        self.remove_widget(self.ti)
        self.parent.remove_widget(self)

    def validate(self, value):
        """
        Validate the creation of the criterion
        """
        if len(value.text) != 0:
            criterion = Critere(0, value.text, self.user, self.pos, self.parent.colored_criterions)
            self.user.add_criterion_lvl(self.parent.current_lvl)
            self.parent.add_criterion(criterion)
            for indicator in self.parent.indicators:
                if indicator.__class__ == PhysicalIndicator:
                    indicator.add_ball(self.user.identifier, self.user.position)
        self.parent.remove_widget(self)
