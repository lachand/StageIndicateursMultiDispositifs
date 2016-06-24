#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from math import pi
from math import sin, cos

from kivy.graphics import Line
from kivy.graphics import Rectangle
from kivy.uix.colorpicker import Color
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget

from Animal import Animal
from Critere import Critere


class Links(Widget):
    """
    A class to view all links on the table
    """

    def __init__(self, integrated):
        """
        Initialize the canvas containing links
        :param integrated: if the links are colored or grey
        """
        self.integrated = integrated
        Widget.__init__(self)
        self.nb_links_users = [0] * 4
        self.label = Label(text='Liens :', size=(75, 15))
        self.label2 = Label(text='Liens :', size=(75, 15))
        self.label3 = Label(text='Liens :', size=(75, 15))
        self.label4 = Label(text='Liens :', size=(75, 15))

    def draw_label(self):
        """
        Draw the label of the link
        """
        if not self.integrated:
            scatter = Scatter(size=self.label.size, pos=(0, 100), do_rotation=False, do_scale=False,
                              do_translation=False, rotation = 270)
            scatter.add_widget(self.label)
            self.add_widget(scatter)

            scatter2 = Scatter(size=self.label.size,
                               pos=(self.get_root_window().width - 100, self.get_root_window().height - 175),
                               do_rotation=False, do_scale=False,
                               do_translation=False, rotation=90)
            scatter2.add_widget(self.label2)
            self.add_widget(scatter2)

            scatter3 = Scatter(size=self.label.size, pos=(0, self.get_root_window().height - 200), do_rotation=False,
                               do_scale=False,
                               do_translation=False, rotation=270)
            scatter3.add_widget(self.label3)
            self.add_widget(scatter3)

            scatter4 = Scatter(size=self.label.size, pos=(self.get_root_window().width - 100, 125), do_rotation=False,
                               do_scale=False,
                               do_translation=False, rotation = 90)
            scatter4.add_widget(self.label4)
            self.add_widget(scatter4)

    def update(self, dt):
        """
        Update the view of links
        :param dt:
        """
        self.canvas.clear()
        for child in self.children:
            self.canvas.add(child.canvas)
        for child in self.parent.children:
            if child.__class__ == Critere:
                for link in child.links:
                    for child2 in self.parent.children:
                        if child2.__class__ == Animal and link.linked_to_animal(child2.identifier):
                            user = self.parent.get_user(link.id_usr)
                            self.nb_links_users[user.identifier - 1] += 1
                            with self.canvas:
                                if self.integrated:
                                    color = user.color
                                    Color(color[0], color[1], color[2])
                                else:
                                    Color(.25, .25, .25)
                                Line(points=[child.center[0], child.center[1], child2.center[0], child2.center[1]],
                                     width=2)
        if not self.integrated:
            self.draw_not_integrated()

    def draw_not_integrated(self):
        """
        Draw the criterion when not in
        :return:
        """
        global position, rotation
        position = (-100, -100)
        rotation = 0
        for user in self.parent.group.users:
            if user.identifier == 1:
                position = 15, 200
                rotation = pi
            elif user.identifier == 2:
                position = self.get_root_window().width - 15, self.get_root_window().height-200
                rotation = 0
            elif user.identifier == 3:
                position = 15, self.get_root_window().height-100
                rotation = pi
            elif user.identifier == 4:
                position = self.get_root_window().width - 15, 100
                rotation = 0

            cpt = 1
            total = (self.nb_links_users[0]) + (self.nb_links_users[1]) + (self.nb_links_users[2]) + (self.nb_links_users[3])
            if total == 0:
                total = 1
            for elmt in self.nb_links_users:
                with self.canvas:
                    user = self.parent.get_user(cpt)
                    color = user.color
                    Color(color[0], color[1], color[2])

                    if rotation == 0:
                        pos = (position[0] + (100 / total) * (cpt * sin(rotation) - cos(rotation) * elmt),
                               position[1] + 20 * (cpt * cos(rotation) - sin(rotation) * elmt))
                        size = (abs(cos(rotation) * elmt / total * 100), 20 + abs(sin(rotation) * elmt) * 20)
                    elif rotation == pi:
                        pos = (position[0], position[1] + 20 * (cpt * cos(rotation) - sin(rotation) * elmt))
                        size = (abs(cos(rotation) * elmt / total * 100), 20 + abs(sin(rotation) * elmt) * 20)
                    Rectangle(size=size, pos=pos)

                cpt += 1
        self.nb_links_users = [0] * 4
