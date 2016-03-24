#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import math

from kivy.clock import Clock
from kivy.graphics import Ellipse
from kivy.uix.colorpicker import Color
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter

from Link import Link
from PhysicalIndicator import PhysicalIndicator


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
        self.size = len(text) + 100, 50
        self.colored = colored
        self.fused = False
        self.last_touch = (0, 0)
        self.vote_activated = False
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
            for indicator in self.parent.indicators:
                if indicator.__class__ == PhysicalIndicator:
                    indicator.add_ball(id_usr, self.parent.group.get_user(id_usr).position)

    def collide_with_zone(self):
        """
        Return if the criterion collides with an user's zone
        :return: True if collide, else False
        """
        print self.parent.user_zones
        for element in self.parent.user_zones:
            if self.collide_widget(element):
                return True
        return False

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

        self.draw_critere(self.fusionneurs, self.size)

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
        """
        Validate the criterion by an user
        :param user: The user that validates the criterion
        :param value: The value for validation
        """
        if not self.validated:
            if self.validator.__contains__(user):
                if value == 0:
                    self.validator.remove(user)
            elif value == 1:
                self.validator.append(user)
            if len(self.validator) == len(self.parent.group.users):
                self.validate()

    def validate(self):
        """
        Validate the criterion
        """
        self.validated = True
        self.vote_activated = False
        self.canvas.clear()
        self.size = self.size[0] - 100, self.size[1] - 100
        self.pos = self.pos[0] + 50, self.pos[1] + 50
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Ellipse(size=(self.size[0] + 10, self.size[1] + 10), pos=(-5, -5))
        self.draw_critere(self.fusionneurs, self.size)

    def draw_critere(self, users, size, pos=(0, 0)):
        """
        Draw a criterion
        :param users: the list of users creating the criterion
        :param size: the size of the criterion
        :param pos: the position of the criterion
        """
        cpt = 0
        for user in users:
            with self.canvas:
                if self.colored:
                    Color(user.color[0], user.color[1], user.color[2])
                    Ellipse(pos=pos, size=size, angle_start=cpt, angle_end=cpt + (360 / (len(self.fusionneurs) + 1)))
                    cpt += 360 / (len(users) + 1)
                else:
                    Color(.25, .25, .25)
                    Ellipse(size=size, angle_start=cpt, angle_end=cpt + (360 / (len(self.fusionneurs) + 1)))
                    cpt += 360 / (len(users) + 1)
        with self.canvas:
            if self.colored:
                Color(self.createur.color[0], self.createur.color[1], self.createur.color[2])
                Ellipse(pos=pos, size=size, angle_start=cpt, angle_end=cpt + (360 / (len(self.fusionneurs) + 1)))
                cpt += 360 / (len(users) + 1)
            else:
                Color(.25, .25, .25)
                Ellipse(pos=pos, size=size, angle_start=cpt, angle_end=cpt + (360 / (len(self.fusionneurs) + 1)))
                cpt += 360 / (len(users) + 1)
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
                                       self.center[
                                           1]) and child.current_user is not None and not self.collide_with_zone():
                    self.add_link(child.identifier, child.current_user.identifier)
                    child.current_user.add_link(self.createur.identifier)
                    child.remove_user()

        for user in self.parent.group.users:
            if user.validate:
                cpt += 1
        if cpt == 4:
            self.canvas.clear()
            for child in self.parent.children:
                if child.__class__ == Critere and child.collide_point(self.center[0], self.center[1]) and child != self:
                    self.fuse_concept(child)

    def on_touch_move(self, touch):
        """
        Define actions to perform when the indicator is moved
        :param touch: the touch point (position, type of touch, ...)
        """
        from Animal import Animal
        for child in self.parent.children:
            if child.__class__ == Animal:
                for link in self.links:
                    if link.linked_to_animal(child.identifier):
                        x = self.center_x + link.distance * math.cos(link.angle + math.pi)
                        y = self.center_y + link.distance * math.sin(-link.angle + math.pi)
                        child.update_coordinate(x,
                                                y)
        Scatter.on_touch_move(self, touch)

    def on_touch_down(self, touch):
        """
        Define actions to perform when the indicator is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if self.collide_point(touch.x, touch.y):
            Scatter.on_touch_down(self, touch)
            self.last_touch = touch.pos
            if self.vote_activated:
                dx = self.center[0] - touch.x
                dy = self.center[1] - touch.y
                angle = (math.atan2(-dy, dx) / (2 * math.pi)) * 360 - 90
                print angle % 360
                for user in self.parent.group.users:
                    x = user.position[0] / self.parent.size[0]
                    y = user.position[1] / self.parent.size[1]
                    if x == 0:
                        if y == 0:
                            angle2 = 180
                        else:
                            angle2 = 270
                    else:
                        if y == 0:
                            angle2 = 90
                        else:
                            angle2 = 0
                    x = 5 + self.size[0] / 3 + self.size[0] / 3 * math.sin(
                        (angle2 + 360. / (self.parent.group.nb_users() * 2.)) / 360. * 2. * math.pi)
                    y = -5 + self.size[1] / 3 + self.size[1] / 3 * math.cos(
                        (angle2 + 360. / (self.parent.group.nb_users() * 2.)) / 360. * 2. * math.pi)

                    with self.canvas:
                        if angle2 < angle % 360 < angle2 + 2 * (360 / (self.parent.group.nb_users() * 2)):
                            Color(user.color[0], user.color[1], user.color[2], 1)
                            Ellipse(size=(self.size[0], self.size[1]), angle_start=angle2,
                                    angle_end=angle2 + 360 / (self.parent.group.nb_users() * 2))
                            angle2tmp = angle2 + 360 / (self.parent.group.nb_users() * 2)
                            Color(user.color[0] / 2., user.color[1] / 2., user.color[2] / 2., 1)
                            Ellipse(size=(self.size[0], self.size[1]), angle_start=angle2tmp,
                                    angle_end=angle2tmp + 360 / (self.parent.group.nb_users() * 2))
                            self.draw_critere(self.fusionneurs, (self.size[0] - 100, self.size[1] - 100), (50, 50))

                    if angle2 < angle % 360 < angle2 + 360 / (self.parent.group.nb_users() * 2):
                        with self.canvas:
                            Image(source="Images/validate.png", pos=(x, y), size=(50, 50), color=(0.93, 0.93, 0.93, .5))
                        self.validate_by_user(user.identifier, 1)

                    elif angle2 + 360 / (self.parent.group.nb_users() * 2) < angle % 360 < angle2 + 2 * (
                                360 / (self.parent.group.nb_users() * 2)):
                        with self.canvas:
                            Image(source="Images/unvalidate.png", pos=(x, y), size=(50, 50), color=(0.5, 0.5, 0.5, .5))
                        self.validate_by_user(user.identifier, 0)
            Clock.schedule_once(self.is_touched, 2)

    def activate_vote(self):
        """
        Activate the voting phase
        """
        self.vote_activated = True
        self.size = self.size[0] + 100, self.size[1] + 100
        self.pos = self.pos[0] - 50, self.pos[1] - 50
        self.canvas.clear()
        for user in self.parent.group.users:
            x = user.position[0] / self.parent.size[0]
            y = user.position[1] / self.parent.size[1]
            if x == 0:
                if y == 0:
                    angle = 180
                else:
                    angle = 270
            else:
                if y == 0:
                    angle = 90
                else:
                    angle = 0
            with self.canvas:
                Color(user.color[0], user.color[1], user.color[2], 1)
                Ellipse(size=(self.size[0], self.size[1]), angle_start=angle,
                        angle_end=angle + 360 / (self.parent.group.nb_users() * 2))
                angle += 360 / (self.parent.group.nb_users() * 2)
                Color(user.color[0] / 2., user.color[1] / 2., user.color[2] / 2., 1)
                Ellipse(size=(self.size[0], self.size[1]), angle_start=angle,
                        angle_end=angle + 360 / (self.parent.group.nb_users() * 2))
                angle += 360 / (self.parent.group.nb_users() * 2)
        self.draw_critere(self.fusionneurs, (self.size[0] - 100, self.size[1] - 100), (50, 50))

    def desactivate_vote(self):
        """
        Desctivate the voting phase
        """
        self.vote_activated = False
        self.size = self.size[0] - 100, self.size[1] - 100
        self.pos = self.pos[0] + 50, self.pos[1] + 50
        self.canvas.clear()
        self.draw_critere(self.fusionneurs, self.size)

    def is_touched(self, dt):
        """
        Activate or desactivate the voting phase in fonction of last touch
        """
        if len(self._touches) == 1:
            if self._touches[0].pos == self.last_touch:
                if not self.validated:
                    if not self.vote_activated:
                        self.activate_vote()
                    else:
                        self.desactivate_vote()
