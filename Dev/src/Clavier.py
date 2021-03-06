#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput

from Critere import Critere


class Clavier(Scatter):
    """
    A class representing a keyboard for criterion creation
    """

    def __init__(self, user, color, position, angle, support, size,criterion=None,text_type="",edition="creation"):
        """
        Initialize the keyboard
        :param user: the user which is creating the criterion
        :param color: the color of the user
        :param position: the position of the keyboard
        :param angle: the angle of the keyboard
        """
        Scatter.__init__(self)
        self.support = support

        self.user = user
        self.identifier = self.user.identifier
        self.color = color
        self.pos = position
        self.rotation = angle
        self.criterion = criterion
        if self.criterion is not None:
            text = criterion.texte
        else :
            text = "Entrez du texte ..."

        if support == "tablette":
            self.ti = TextInput(size_hint=(None, None), multiline=True, text=text,font_size=40, pos=(position[0],size[1]-position[1]-(size[1]/3)) ,size = (size[0],size[1]/3),
                                text_size=self.size)
        else:
            self.ti = TextInput(size_hint=(None, None), multiline=False, size=(100, 30), text=text, focus=False,text_size=self.size)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False
        self.ti.background_color = self.color + [1]
        self.ti.foreground_color = [1, 1, 1, 1]
        self.text_type = text_type

    def initialisation(self):
        """
        Initialize the keyboard
        """
        self.parent.add_widget(self.ti)
        self.parent.edition_mode = True

    def destroy(self):
        """
        Destroy the keyboard
        :param value:
        """
        self.parent.edition_mode = False
        self.ti.focus = False
        self.parent.remove_widget(self.ti)
        self.parent.remove_widget(self)

    def validate(self, text_type):
        """
        Validate the creation of the criterion
        :param value:
        """
        self.text_type = text_type

        if len(self.ti.text) != 0:
            if self.criterion is None:
                criterion = Critere(0, self.ti.text, self.user, self.pos, self.parent.integrated_criterions, self.support, text_type=self.text_type)
                self.parent.add_criterion(criterion)
                self.user.add_criterion_lvl(self.parent.current_lvl)
            else:
                self.criterion.texte = self.ti.text
                self.parent.logger.write("edit_critere", self.user.identifier, [self.criterion.createur.identifier])
                self.criterion.pos = 0,0
