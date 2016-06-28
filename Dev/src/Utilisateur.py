#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

class Utilisateur:
    """
    A class representing a user of the application
    """

    def __init__(self, identifier, color, max_lvl=3, pos=(50, 50)):
        """
        Initialize an user
        :param identifier: the identifier of the user
        :param color: the color of the user
        :param max_lvl: the max_lvl for objectives
        """
        self.identifier = identifier
        self.color = color
        self.validate = False
        self.criterion = []
        self.nb_criterions = [0, 0, 0, 0]
        self.nb_criterion = 0
        self.current_image = None
        self.links_persos = 0
        self.links_others = 0
        self.max_lvl = max_lvl
        self.position = pos
        self.socket = None
        self.votes = []
        self.name = ""

        for i in range(0, max_lvl):
            self.nb_criterions.append(0)

    def has_criterion(self, id_criterion):
        """
        Return if the user is the creator of a specified criterion
        :param id_criterion: the identifier of the criterion
        :return: true if hte user is the creator, else false
        """
        if self.criterion.__getitem__(id_criterion).size == 0:
            return False
        else:
            return True

    def add_link(self, identifier):
        """
        add a link to statistics
        :param identifier: the identifier of the link
        """
        if identifier != self.identifier:
            self.links_others += 1
        else:
            self.links_persos += 1

    def add_criterion(self, id_criterion):
        """
        add a criterion to statistics
        :param id_criterion: the identifier of the criterion
        """
        self.criterion.append(id_criterion)

    def add_criterion_lvl(self, level):
        """
        add a criterion to statistics
        :param level : the current level of the game
        """
        self.nb_criterions[level] += 1
        self.nb_criterion += 1

    def add_socket(self, newsock):
        self.socket = newsock
