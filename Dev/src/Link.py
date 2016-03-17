#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import math


class Link:
    """
    A class representing a link between an animal and a criterion
    """
    def __init__(self, id_img, id_usr):
        """
        Initialization of a link
        :param id_img: the id of the image to link
        :param id_usr: the id of the user creating the link
        """
        self.id_img = id_img
        self.id_usr = id_usr
        self.distance = 0
        self.angle = 0

    def linked_to(self, id_img, id_usr):
        """
        Return if the link is between a specified animal and a specified user
        :param id_img: the id of the specified animal
        :param id_usr: the id of the specified user
        :return: true if the link exists, else false
        """
        return self.id_img == id_img and self.id_usr == id_usr

    def linked_to_animal(self, id_img):
        """
        Return if the link is between a specified animal
        :param id_img: the id of the specified animal
        :return: true if the link exists, else false
        """
        return self.id_img == id_img

    def linked_to_user(self, id_usr):
        """
        Return if the link is between a specified user
        :param id_usr: the id of the specified user
        :return: true if the link exists, else false
        """
        return self.id_usr == id_usr

    def update(self, center_animal, center_criterion):
        """
        Update the distance and angle of the link
        :param center_animal: the center of the animal
        :param center_criterion: the center of the criterion
        """
        dx = center_criterion[0] - center_animal[0]
        dy = center_criterion[1] - center_animal[1]

        self.distance = math.hypot(dx, dy)
        self.angle = math.atan2(-dy, dx)
