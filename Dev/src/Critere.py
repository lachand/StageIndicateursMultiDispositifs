#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import math

from kivy.graphics import Rectangle
from kivy.uix.colorpicker import Color
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter

from Link import Link


class Critere(Scatter):
    """
    A class to represent a criterion
    """

    def __init__(self, identifier, text, creator, position, integrated, support="table", fusionneurs = [], text_type=""):
        """
        Initialize a criterion
        :param identifier: the identifier of the criterion
        :param text: the text of the criterion
        :param creator: the creator of the criterion
        :param position: the position of the criterion
        :param integrated: if the criterion is colored or in grey
        """
        Scatter.__init__(self)
        self.support = support
        self.fusionneurs = fusionneurs

        self.pos = position
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
        if self.support == "tablette":
            self.size=400,400
        else:
            self.size = 100,100
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

        if creator.identifier == 1 and self.support != "tablette":
            self.rotation = 0
        elif creator.identifier == 2 and self.support != "tablette":
            self.rotation = 180
        elif creator.identifier == 3 and self.support != "tablette":
            self.rotation = 180
        elif creator.identifier == 4 and self.support != "tablette":
            self.rotation = 0

    def draw(self):
        """
        Draw the criterion
        """
        self.canvas.clear()

        if self.validated:
             self.canvas.clear()
             with self.canvas:
                 Color(1, 1, 1, 1)
                 Rectangle(size=(self.size[0] + 10, self.size[1] + 10), pos=(-5, -5))

        with self.canvas:

            Color(0, 0, 0, 1)
            Rectangle(size=(self.size[0] + 4, self.size[1] + 4), pos=(-2, -2))
            Color(.25, .25, .25)

            Rectangle(size=self.size)

            if self.support != "tablette":
                cpt = 0
                for user in self.parent.group.users:
                    Color(user.color[0], user.color[1], user.color[2])
                    print "user :"
                    print user
                    print "validator :"
                    print self.validator
                    print "supress :"
                    print self.suppression
                    if self.validator.count(user.identifier) > 0:
                        texture = self.parent.image_user_yes.texture
                    elif self.suppression.count(user.identifier) > 0:
                        texture = self.parent.image_user_no.texture
                    else:
                        texture = self.parent.image_user.texture
                    Rectangle(texture=texture, size=(self.size[0] / 5, self.size[1] / 5),
                          pos=(cpt * (self.size[1] / 5), self.size[1] - self.size[1] / 5))
                    if len(user.name) > 0:
                        Label(size=(self.size[0] / 5,self.size[1] / 5),text=user.name[0], color=(1, 1, 1, 1), pos=(cpt * (self.size[1] / 5), self.size[1] - self.size[1] / 4),valign='bottom')
                    cpt += 1
                Color(0.5, 0.5, 0.5, 1)
                Rectangle(size=(self.size[0], 2),pos=(0,self.size[1] - self.size[1] / 5))

            if self.integrated:
                Color(self.createur.color[0], self.createur.color[1], self.createur.color[2])
                Rectangle(size=(self.size[0]/4,self.size[1]/6), pos=(0,0))
                cpt = 1
                for fusionneur in self.fusionneurs:
                    Color(fusionneur.color[0], fusionneur.color[1], fusionneur.color[2])
                    Rectangle(size=(self.size[0] / 4, self.size[1] / 6),
                              pos=(cpt*(self.size[0] / 4), 0))
                    cpt += 1
                Color(0.5, 0.5, 0.5, 5)
                Rectangle(size=(self.size[0], 2),
                          pos=(0, self.size[1]/6))
            Label(text=str(self.text_type), halign='left', color=(1, 1, 1, 1),size=self.size,text_size=(self.size[0],self.size[1]-2*self.size[1]/5), valign='top', pos=(0,0))
            Color(0.5, 0.5, 0.5, 1)
            Rectangle(size=(self.size[0], 2), pos=(0, self.size[1] - self.size[1] / 5 - 20))

            Label(text=self.texte, halign='left', size=self.size, color=(1, 1, 1, 1),text_size=(self.size[0],self.size[1]-3.5*self.size[1]/5),valign='top',pos=(0,0))


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
                    # if link.linked_to_user(id_usr):
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
        if not self.validated and not self.destroyed and not self.parent is None:
            self.parent.logger.write("vote", user, [value, self.createur.identifier])
            if value == 0:
                if self.validator.count(user) > 0:
                    self.validator.remove(user)
                    self.parent.group.get_user(user).votes.remove(1)
                if self.suppression.count(user) == 0:
                    self.suppression.append(user)
                    self.parent.group.get_user(user).votes.append(value)
            elif value == 1:
                if self.suppression.count(user) > 0:
                    self.suppression.remove(user)
                    self.parent.group.get_user(user).votes.remove(0)
                if self.validator.count(user) == 0:
                    self.validator.append(user)
                    self.parent.group.get_user(user).votes.append(value)
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
            self.draw()

    def draw_critere(self, users, size, pos=(0, 0)):
        """
        Draw a criterion
        :param users: the list of users creating the criterion
        :param size: the size of the criterion
        :param pos: the position of the criterion
        """
        self.canvas.clear()
        if not self.destroyed:
            cpt = 0
            with self.canvas:
                Color(0, 0, 0, 1)
                Rectangle(size=(size[0] + 4, size[1] + 4), pos=(pos[0] - 2, pos[1] - 2))


            if self.validated:
                self.canvas.clear()
                with self.canvas:
                    Color(1, 1, 1, 1)
                    Rectangle (size=(self.size[0] + 10, self.size[1] + 10), pos=(-5, -5))

            with self.canvas:
                Color(.25, .25, .25)
                Rectangle(size=self.size)

                if self.integrated:
                    Color(self.createur.color[0], self.createur.color[1], self.createur.color[2])
                    if self.validator.count(self.createur) > 0:
                        texture = self.yes.texture
                    elif self.suppression.count(self.createur) > 0:
                        texture = self.no.texture
                    else :
                        texture = self.parent.image_user.texture
                    Rectangle(texture=texture, size=(self.size[0] / 5, self.size[1] / 5),
                              pos=(0, self.size[1] - self.size[1] / 5))
                    cpt = 1
                    for fusionneur in self.fusionneurs:
                        if self.validator.count(fusionneur) > 0:
                            texture = self.yes.texture
                        elif self.suppression.count(fusionneur) > 0:
                            texture = self.no.texture
                        else:
                            texture = self.parent.image_user.texture
                        Color(fusionneur.color[0], fusionneur.color[1], fusionneur.color[2])
                        Rectangle(texture=texture, size=(self.size[0] / 5, self.size[1] / 5),
                                  pos=(cpt * (self.size[1] / 5), self.size[1] - self.size[1] / 5))
                        cpt += 1

                Label(text=str(self.text_type), halign='left', color=(1, 1, 1, 1),
                      pos=(0, self.size[1] - 1.8 * self.size[1] / 5), valign='top')

                Label(text=self.texte, halign='left', size=self.size, color=(1, 1, 1, 1),
                      text_size=(self.size[0], self.size[1] - 2.6 * self.size[1] / 5.), valign='top', pos=(0, 0))


    def update(self, dt):
        """
        Update the criterion
        :param dt:
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
        Define actions to perform when the indicator is moved
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
                Scatter.on_touch_move(self, touch)

    def on_touch_up(self, touch):
        """
            Define actions to perform when the indicator is touched up
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
                        self.parent.remove_widget(self)

            Scatter.on_touch_up(self, touch)
            if self.rotation is not True:
                self.rotation_value = self.rotation

    def on_touch_down(self, touch):
        """
        Define actions to perform when the indicator is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if not self.destroyed:
            if self.collide_point(touch.x, touch.y):
                Scatter.on_touch_down(self, touch)

                if touch.is_double_tap and self.support != "tablette":
                    if self.zoom_mode:
                        self.size = (100,100)
                        self.draw()
                        self.zoom_mode = False
                    else:
                        self.size = (400, 400)
                        self.draw()
                        self.zoom_mode = True
                if touch.is_double_tap and self.support == "tablette":
                    self.draw_critere(self.fusionneurs, self.size)
                if self.vote_activated and not self.in_ellipse((touch.x, touch.y), self.center,
                                                               (self.size[0] - 100, self.size[1] - 100)):
                    dx = self.center[0] - touch.x
                    dy = self.center[1] - touch.y
                    angle = (math.atan2(-dy, dx) / (2 * math.pi)) * 360 - 90
                    for user in self.parent.group.users:
                        if user is not None and self.parent is not None:
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

                            if angle2 < angle % 360 < angle2 + 360 / (self.parent.group.nb_users() * 2):
                                self.validate_by_user(user.identifier, 1)
                                self.draw_during_vote()

                            elif angle2 + 360 / (self.parent.group.nb_users() * 2) < angle % 360 < angle2 + 2 * (
                                        360 / (self.parent.group.nb_users() * 2)):
                                self.validate_by_user(user.identifier, 0)
                                self.draw_during_vote()

    def is_touched(self, dt):
        """
        Activate or desactivate the voting phase in fonction of last touch
        :param dt:
        """
        if not self.destroyed:
            if len(self._touches) == 1 and self.support == "table":
                if (self.last_touch[0] - 10 <= self._touches[0].pos[0] <= self.last_touch[0] + 10) and (
                                    self.last_touch[1] - 10 <= self._touches[0].pos[1] <= self.last_touch[1] + 10):
                    if not self.validated:
                        if not self.vote_activated:
                            self.activate_vote()
                        else:
                            self.desactivate_vote()

    def in_ellipse(self, point, ellipse_center, ellipse_size):
        """
        Return if the touch is in the ellipse or not
        :param point: the point to test
        :param ellipse_center: the center of the ellipse
        :param ellipse_size: the size of the ellipse
        :return: if the touch is in the ellipse or not
        """
        if not self.destroyed:
            return math.pow((point[0] - ellipse_center[0]), 2) / math.pow(ellipse_size[0] / 2., 2) + math.pow((point[1] - ellipse_center[1]), 2) / math.pow(ellipse_size[1] / 2., 2) <= 1
