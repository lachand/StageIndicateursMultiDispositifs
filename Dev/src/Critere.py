#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import math

from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter

from Link import Link


class Critere(Scatter):
    """
    A class to represent a criterion
    """
    source_user1 = StringProperty('Images/user.png')
    source_user2 = StringProperty('Images/user.png')
    source_user3 = StringProperty('Images/user.png')
    source_user4 = StringProperty('Images/user.png')

    color_user1 = ListProperty([1, 1, 1])
    color_user2 = ListProperty([1, 1, 1])
    color_user3 = ListProperty([1, 1, 1])
    color_user4 = ListProperty([1, 1, 1])

    color_validated = ListProperty([0,0,0])

    color_user_edit1 = ListProperty([.25, .25, .25])
    color_user_edit2 = ListProperty([.25, .25, .25])
    color_user_edit3 = ListProperty([.25, .25, .25])
    color_user_edit4 = ListProperty([.25, .25, .25])

    color_separator = ListProperty([.25, .25, .25])

    question_text = StringProperty("")

    size_separator = NumericProperty(10)

    label_text_pos =  ListProperty([0,0])
    label_text_size = ListProperty([0,0])
    label_question_pos = ListProperty([0,0])
    label_question_size = ListProperty([0,0])

    def __init__(self, identifier, text, creator, position, integrated, support="table", fusionneurs = [], text_type=""):
        """
        Initialize a criterion
        :param identifier: the identifier of the criterion
        :param text: the text of the criterion
        :param creator: the creator of the criterion
        :param position: the position of the criterion
        :param integrated: if the criterion is colored or in grey
        """

        self.support = support
        self.fusionneurs = fusionneurs

        self.nb_liaisons = 0
        self.identifier = identifier
        self.texte = text
        self.createur = creator
        self.fusionneurs = fusionneurs
        self.validator = []
        self.suppression = []
        self.validated = False
        self.color = self.createur.color
        self.links = []
        self.question_text = text_type

        if self.support == "tablette":
            self.size=400,400
        else:
            self.size = 120,120
            if integrated:
                self.color_separator = [0.5,0.5,0.5]

        self.integrated = integrated
        self.fused = False
        self.last_touch = (0, 0)
        self.vote_activated = False
        self.do_scale = False
        self.rotation_value = 0
        self.yes = Image(source="Images/user_validate.png")
        self.no = Image(source="Images/user_unvalidate.png")
        self.destroyed = False
        self.parent_height = position[1]+100
        self.zoom_mode = False
        self.text_type = text_type
        self.text=text

        if creator.identifier == 1 and self.support != "tablette":
            self.rotation = 0
        elif creator.identifier == 2 and self.support != "tablette":
            self.rotation = 180
        elif creator.identifier == 3 and self.support != "tablette":
            self.rotation = 180
        elif creator.identifier == 4 and self.support != "tablette":
            self.rotation = 0

        self.label_text_pos = [5, 5+self.size[1]/5]
        self.label_text_size = [self.size[0] - 10, self.size[1]-30 - 2*self.size[1]/5]
        self.label_question_pos = [5,self.size[1]-self.size[1]/5 - 25]
        self.label_question_size = [self.size[0]-10,20]

        self.label_question = Label(text=text_type, text_size=self.label_question_size, pos=self.label_question_pos, halign="left", valign= 'top', size= self.label_question_size)
        self.label_text = Label(text=text, text_size=self.label_text_size, pos=self.label_text_pos, valign='top', halign="left", size_hint_y=None, multiline=True, size=self.label_text_size)
        self.size_separator = self.label_question.font_size

        self.color_user_edit1 = self.createur.color

        Scatter.__init__(self)
        self.pos = position[0], position[1] + 200
        self.add_widget(self.label_question)
        self.add_widget(self.label_text)

    def draw(self):
        """
        First draw of the criterion
        :return:
        """

        if self.support != "tablette":
            for user in self.parent.group.users:
                if user.identifier == 1:
                    self.color_user1 = [user.color[0], user.color[1], user.color[2]]
                elif user.identifier == 2:
                    self.color_user2 = [user.color[0], user.color[1], user.color[2]]
                if user.identifier == 3:
                    self.color_user3 = [user.color[0], user.color[1], user.color[2]]
                else:
                    self.color_user4 = [user.color[0], user.color[1], user.color[2]]
        else:
            for user in self.parent.group.users:
                if user.identifier == 1:
                    self.color_user1 = [user.color[0], user.color[1], user.color[2]]
                elif user.identifier == 2:
                    self.color_user2 = [user.color[0], user.color[1], user.color[2]]
                if user.identifier == 3:
                    self.color_user3 = [user.color[0], user.color[1], user.color[2]]
                else:
                    self.color_user4 = [user.color[0], user.color[1], user.color[2]]


    def add_link(self, id_img, id_usr, distance=0, angle=0):
        """
        Add a link between the criterion and an animal
        :param angle:
        :param distance:
        :param id_img: the identifier of the animal
        :param id_usr: the identifier of the user focusing the animal
        """
        if not self.destroyed :
            est_dedans = False
            for link in self.links:
                if link.linked_to_animal(id_img):
                    est_dedans = True
                    tab = [link.id_usr, self.createur.identifier]
                    for fusionneur in self.fusionneurs:
                        tab.append(fusionneur.identifier)
                    self.parent.logger.write("destroy_link", id_usr, tab)
                    self.links.remove(link)
            if not est_dedans:
                self.links.append(Link(id_img, id_usr, distance, angle))
                tab = [self.createur.identifier]
                for fusionneur in self.fusionneurs:
                    tab.append(fusionneur.identifier)
                self.parent.logger.write("create_link", id_usr, tab)

    def collide_with_zone(self):
        """
        Return if the criterion collides with an user's zone
        :return: True if collide, else False
        """
        from Table import Table
        if not self.destroyed :
            if self.parent.__class__ == Table:
                for element in self.parent.user_zones:
                    if self.collide_widget(element):
                        return True
        return False

    def fuse_concept(self, concept):
        pass
        """
        Fuse two criterions together
        :param concept: the other criterion ton fuse
        """
        if self.createur.identifier != concept.createur.identifier and not self.destroyed:
            if not self.fusionneurs.__contains__(concept.createur):
                self.fusionneurs.append(concept.createur)
                self.parent.criterions[self.parent.criterions.index(concept)].fused = True

        for fusionneur in concept.fusionneurs:
            if self.createur.identifier != fusionneur.identifier and not self.destroyed:
                if not self.fusionneurs.__contains__(fusionneur):
                    self.fusionneurs.append(fusionneur)
                    self.parent.criterions[self.parent.criterions.index(concept)].fused = True

        for link in concept.links:
            if self.has_link(link.id_img) == -1 and not self.destroyed:
                self.add_link(link.id_img, link.id_usr)

        for fils in self.parent.children:
            if fils.__class__ == Critere and fils.collide_widget(self) and fils != self and not self.destroyed:
                self.parent.remove_widget(fils)

    def has_link(self, identifier):
        """
        Return if the criterion is linked to a specified animal
        :param identifier: The identifier of the animal
        :return: the position of the animal in the link's table or -1 if the criterion is not linked to the animal
        """
        if not self.destroyed:
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
        if not self.destroyed:
            self.links[index].update(center, self.center)

    def validate_by_user(self, user, value):
        """
        Validate the criterion by an user
        :param user: The user that validates the criterion
        :param value: The value for validation
        """
        if not self.validated and not self.destroyed:
            self.parent.logger.write("vote", user, [value, self.createur.identifier])
            if value == 0:
                if self.validator.count(user) > 0:
                    self.validator.remove(user)
                    self.parent.group.get_user(user).votes.remove(1)
                if self.suppression.count(user) == 0:
                    self.suppression.append(user)
                    self.parent.group.get_user(user).votes.append(value)
                source = "Images/user_unvalidate.png"

            elif value == 1:
                if self.suppression.count(user) > 0:
                    self.suppression.remove(user)
                    self.parent.group.get_user(user).votes.remove(0)
                if self.validator.count(user) == 0:
                    self.validator.append(user)
                    self.parent.group.get_user(user).votes.append(value)
                source = "Images/user_validate.png"

            if user == 1:
                self.source_user1 = source
            elif user == 2:
                self.source_user2 = source
            elif user == 3:
                self.source_user3 = source
            else:
                self.source_user4 = source

            if len(self.validator) == len(self.parent.group.users):
                self.validate()
            elif len(self.suppression) == len(self.parent.group.users):
                self.destroyed = True
                self.links = []
                tab = [self.createur.identifier]
                for fusionneur in self.fusionneurs:
                    tab.append(fusionneur)
                self.parent.logger.write("critere_destroyed", "all", tab)
                self.parent.remove_widget(self)
                pass

    def validate(self):
        """
        Validate the criterion
        """
        if not self.destroyed:
            self.validated = True
            self.vote_activated = False
            self.color_validated= [1,1,1]

    def update(self, dt):
        """
        Update the criterion
        """
        if self.support != "tablette" :
            from Animal import Animal
            from Table import Table
            if not self.destroyed:
                cpt = 0
                for child in self.parent.children:
                    if child.__class__ == Animal:
                        if child.collide_point(self.center[0],
                                               self.center[
                                                   1]) and child.current_user is not None:
                            self.add_link(child.identifier, child.current_user.identifier)
                            child.current_user.add_link(self.createur.identifier)
                            child.remove_user()

                if self.parent.__class__.__name__ == Table.__name__:
                    for user in self.parent.group.users:
                        if user.validate:
                            cpt += 1
                    if cpt == 4:
                        for child in self.parent.children:
                            if child.__class__ == Critere and child.collide_point(self.center[0],
                                                                                  self.center[1]) and child != self:
                                self.fuse_concept(child)


    def on_touch_move(self, touch):
        """
        Defines actions to perform when the criterion is moved
        :param touch: the touch point (position, type of touch, ...)
        """
        from Animal import Animal
        if not self.destroyed:
            if self.parent is not None:
                for child in self.parent.children:
                    if child.__class__ == Animal:
                        for link in self.links:
                            if link.linked_to_animal(child.identifier):
                                x = self.center_x + link.distance * math.cos(link.angle + math.pi)
                                y = self.center_y + link.distance * math.sin(-link.angle + math.pi)
                                child.update_coordinate(x,
                                                        y)
            if self.collide_point(touch.pos[0],touch.pos[1]):
                if self.support == "tablette":

                    if (touch.pos[1]) >= (self.parent.height - 200) :
                        self.send_to_table()
                Scatter.on_touch_move(self, touch)

    def send_to_table(self):
        data = '{"Criterion" : "' + self.texte + '", "IdUser" : "' + str(
            self.parent.user.identifier) + '", "TextType" : "' + self.text_type + '", "Links" : ['
        for link in self.links:
            data += '{ "IdImage" :"' + str(link.id_img) + '",'
            data += '"IdUser" :"' + str(link.id_usr) + '",'
            data += '"Distance" :"' + str(link.distance) + '",'
            data += '"Angle" :"' + str(link.angle) + '"},'
            self.parent.remove_animal(link.id_img)
        if len(self.links) > 0:
            data = data[:-1]
        data += '], "Fusionneurs" : ['
        if self.createur.identifier != self.parent.user.identifier:
            data += '{"IdUser" : "' + str(self.createur.identifier) + '"},'
        for participants in self.fusionneurs:
            data += '{"IdUser" : "' + str(participants.identifier) + '"},'
        if len(self.fusionneurs) > 0 or self.createur.identifier != self.parent.user.identifier:
            data = data[:-1]
        data += ']}\n'
        self.parent.client.send_msg(data)
        self.canvas.clear()
        self.destroyed = True
        self.parent.remove_widget(self)

    def on_touch_up(self, touch):
        """
        Defines action whe the criterion is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if not self.destroyed:
            from ZoneUtilisateur import ZoneUtilisateur
            if self.collide_point(touch.x, touch.y) and self.parent is not None and self.support != "tablette" and not self.validated:
                for child in self.parent.children:
                    if child.__class__ == ZoneUtilisateur and child.collide_point(self.center[0], self.center[1]) and child.is_connected():
                        data = '{"Criterion" : "' + self.texte + '", "IdUser" : "' + str(
                            self.createur.identifier) + '", "TextType" : "' + self.text_type + '", "Links" : ['
                        for link in self.links:
                            data += '{ "IdImage" :"' + str(link.id_img) + '",'
                            data += '"SrcImage" : "' + self.parent.get_animal(link.id_img).src_image + '",'
                            data += '"IdUser" :"' + str(link.id_usr) + '",'
                            data += '"Distance" :"' + str(link.distance) + '",'
                            data += '"Angle" :"' + str(link.angle) + '"},'
                        if len(self.links) > 0:
                            data = data[:-1]

                        data += '], "Fusionneurs" : ['
                        for participants in self.fusionneurs:
                            data += '{"IdUser" : "' + str(participants.identifier) + '"},'
                        if len(self.fusionneurs) > 0 :
                           data = data[:-1]
                        data += ']}\n'
                        self.parent.server.send_msg(data, child.user.socket)
                        self.canvas.clear()
                        self.destroyed = True
                        self.parent.criterions.remove(self)
                        self.parent.remove_widget(self)

            Scatter.on_touch_up(self, touch)

    def on_touch_down(self, touch):
        """
        Defines actions to perform when the criterion is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if not self.destroyed:
            if self.collide_point(touch.x, touch.y):
                Scatter.on_touch_down(self, touch)

                if touch.is_double_tap and self.support != "tablette":
                    if self.zoom_mode:
                        self.size = (120,120)
                        self.zoom_mode = False
                    else:
                        self.size = (400, 400)
                        self.zoom_mode = True
                    self.remove_widget(self.label_question)
                    self.remove_widget(self.label_text)
                    self.label_text_pos = [5, 5 + self.size[1] / 5]
                    self.label_text_size = [self.size[0] - 10, self.size[1] - 30 - 2 * self.size[1] / 5]
                    self.label_question_pos = [5, self.size[1] - self.size[1] / 5 - 25]
                    self.label_question_size = [self.size[0] - 10, 20]

                    self.label_question = Label(text=self.text_type, text_size=self.label_question_size,
                                                pos=self.label_question_pos, halign="left", valign='top',
                                                size=self.label_question_size)
                    self.label_text = Label(text=self.text, text_size=self.label_text_size, pos=self.label_text_pos,
                                            valign='top', halign="left", size_hint_y=None, multiline=True,
                                            size=self.label_text_size)
                    self.add_widget(self.label_question)
                    self.add_widget(self.label_text)