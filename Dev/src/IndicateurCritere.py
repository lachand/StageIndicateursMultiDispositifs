#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.graphics import Ellipse
from kivy.uix.colorpicker import Color
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget

from Critere import Critere


class IndicateurCritere(Widget):
    """
    A class representing an indicator representing the number of criterion created by users
    """

    def __init__(self):
        """
        Initialize the indicator
        """
        Widget.__init__(self)
        self.nb_criterions_users = [0] * 4
        self.label = Label(text='Réponses :',size=(75,15))
        self.label2 = Label(text='Réponses :', size=(75, 15))
        self.label3 = Label(text='Réponses :', size=(75, 15))
        self.label4 = Label(text='Réponses :', size=(75, 15))


    def add_label(self):
        """
        Add labels to the indicator
        """

        scatter = Scatter(size=self.label.size, pos=(0,0), do_rotation=False, do_scale=False,
                          do_translation=False)
        scatter.add_widget(self.label)
        self.add_widget(scatter)


        scatter2 = Scatter(size=self.label.size, pos=(self.get_root_window().width - 100, self.get_root_window().height - 100), do_rotation=False, do_scale=False,
                            do_translation=False, rotation = 180)
        scatter2.add_widget(self.label2)
        self.add_widget(scatter2)

        scatter3 = Scatter(size=self.label.size, pos=(-25, self.get_root_window().height - 100), do_rotation=False, do_scale=False,
                           do_translation=False, rotation=180)
        scatter3.add_widget(self.label3)
        self.add_widget(scatter3)

        scatter4 = Scatter(size=self.label.size, pos=(self.get_root_window().width - 75, 0), do_rotation=False, do_scale=False,
                           do_translation=False)
        scatter4.add_widget(self.label4)
        self.add_widget(scatter4)

    def update(self):
        """
        Update the visualization when a new criterion is added
        """
        global position, rotation
        for critere in self.parent.children:
            if critere.__class__ == Critere:
                self.nb_criterions_users[critere.createur.identifier - 1] += 1
                for fusionneur in critere.fusionneurs:
                    self.nb_criterions_users[fusionneur.identifier - 1] += 1

        for user in self.parent.group.users:
            if user.identifier == 1:
                position = 10, 15
                rotation = 0
            elif user.identifier == 2:
                position = self.get_root_window().width - 60, self.get_root_window().height - 65
                rotation = 180
            elif user.identifier == 3:
                position = 10, self.get_root_window().height - 65
                rotation = 180
            elif user.identifier == 4:
                position = self.get_root_window().width - 60, 15
                rotation = 0

            total = 0
            angle = 0
            for nb in self.nb_criterions_users:
                total += nb

            cpt = 1

            if total > 0 :
                for elmt in self.nb_criterions_users:
                    with self.canvas:
                        user = self.parent.get_user(cpt)
                        color = user.color
                        Color(color[0], color[1], color[2])
                        Ellipse(size=(50, 50), pos=position, angle_start=angle, angle_stop=angle + elmt * 360. / total)
                    angle += elmt * 360. / total
                    cpt += 1
        self.nb_criterions_users = [0] * 4
