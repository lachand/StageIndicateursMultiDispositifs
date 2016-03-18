#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import math

from kivy.graphics import Ellipse
from kivy.uix.colorpicker import Color
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter

from Link import Link


class Critere(Scatter):
    """
    A class to represent a criterion
    """
    def __init__(self, identifier, text, creator, position, colored):
        """
        Initialize a criterion
        :param identifier: the identifier of the criterion
        :param text: the text of the criterion
        :param creator: the creator of the criterion
        :param position: the position of the criterion
        :param colored: if the criterion is colored or in grey
        """
        Scatter.__init__(self)
        self.pos = position
        self.nb_liaisons = 0
        self.identifier = identifier
        self.texte = text
        self.createur = creator
        self.fusionneurs = []
        self.validator = []
        self.validated = False
        self.color = self.createur.color
        self.links = []
        self.size = len(text) * 1 + 100, 50
        self.colored = colored
        self.fused = False
        with self.canvas:
            if self.colored:
                Color(self.color[0], self.color[1], self.color[2])
            else:
                Color(.25, .25, .25)
            Ellipse(size=self.size)
            Label(text=self.texte, halign='left', size=self.size)

    def add_link(self, id_img, id_usr):
        """
        Add a link between the criterion and an animal
        :param id_img: the identifier of the animal
        :param id_usr: the identifier of the user focusing the animal
        """
        est_dedans = False
        for link in self.links:
            if link.linked_to_animal(id_img):
                est_dedans = True
                if link.linked_to_user(id_usr):
                    self.links.remove(link)
        if not est_dedans:
            self.links.append(Link(id_img, id_usr))

    def fuse_concept(self, concept):
        """
        Fuse two criterions together
        :param concept: the other criterion ton fuse
        """
        if self.createur.identifier != concept.createur.identifier:
            if not self.fusionneurs.__contains__(concept.createur):
                self.fusionneurs.append(concept.createur)
                self.parent.criterions[self.parent.criterions.index(concept)].fused = True

        for fusionneur in concept.fusionneurs:
            if self.createur.identifier != fusionneur.identifier:
                if not self.fusionneurs.__contains__(fusionneur):
                    self.fusionneurs.append(fusionneur)
                    self.parent.criterions[self.parent.criterions.index(concept)].fused = True

        for link in concept.links:
            if self.has_link(link.id_img) == -1:
                self.add_link(link.id_img, link.id_usr)

        for fils in self.parent.children:
            if fils.__class__ == Critere and fils.collide_widget(self) and fils != self:
                self.parent.remove_widget(fils)

        cpt = 0
        for fusionneur in self.fusionneurs:
            with self.canvas:
                if self.colored:
                    Color(fusionneur.color[0], fusionneur.color[1], fusionneur.color[2])
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
                else:
                    Color(.25, .25, .25)
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
        with self.canvas:
            if self.colored:
                    Color(self.createur.color[0], self.createur.color[1], self.createur.color[2])
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
            else:
                    Color(.25, .25, .25)
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)

            Label(text=self.texte, halign='left', size=self.size)


    def has_link(self, identifier):
        """
        Return if the criterion is linked to a specified animal
        :param identifier: The identifier of the animal
        :return: the position of the animal in the link's table or -1 if the criterion is not linked to the animal
        """
        for link in self.links:
            if link.linked_to_animal(identifier):
                return self.links.index(link)
        return -1

    def update_link(self, index, center):
        """
        Update the distance and angle between an animal and the criterion
        :param index: the index of hte animal
        :param center: the center of the animal
        """
        self.links[index].update(center, self.center)

    def validate_by_user(self, user, value):
        if not self.validated:
            if self.validator.__contains__(user) :
                if value == 0:
                    self.validator.remove(user)
            elif value == 1:
                self.validator.append(user)
            if len(self.validator) == len(self.parent.group.users):
                self.validate()

    def validate(self):
        self.validated = True
        cpt = 0
        with self.canvas:
            Color(1, 1, 1, 1)
            Ellipse(size=(self.size[0]+10,self.size[1]+10),pos=(-5,-5))

        for fusionneur in self.fusionneurs:
            with self.canvas:
                if self.colored:
                    Color(fusionneur.color[0], fusionneur.color[1], fusionneur.color[2])
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
                else:
                    Color(.25, .25, .25)
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
        with self.canvas:
            if self.colored:
                    Color(self.createur.color[0], self.createur.color[1], self.createur.color[2])
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
            else:
                    Color(.25, .25, .25)
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)

            Label(text=self.texte, halign='left', size=self.size)

    def update(self, dt):
        """
        Update the criterion
        """
        from Animal import Animal
        cpt = 0
        for child in self.parent.children:
            if child.__class__ == Animal:
                if child.collide_point(self.center[0],
                                       self.center[1]) and child.current_user is not None:
                    self.add_link(child.identifier, child.current_user.identifier)
                    child.current_user.add_link(self.createur.identifier)
                    child.remove_user()

        for user in self.parent.group.users:
            if user.validate:
                cpt += 1
        if cpt == 4:
            for child in self.parent.children:
                if child.__class__ == Critere and child.collide_point(self.center[0], self.center[1]) and child != self:
                    self.fuse_concept(child)

    def on_touch_move(self, touch):
        from Animal import Animal
        for child in self.parent.children:
            if child.__class__ == Animal:
                for link in self.links:
                    if link.linked_to_animal(child.identifier):
                        x = self.center_x + link.distance*math.cos(link.angle+math.pi)
                        y = self.center_y + link.distance*math.sin(-link.angle+math.pi)
                        child.update_coordinate(x,
                                                y)
        Scatter.on_touch_move(self, touch)
