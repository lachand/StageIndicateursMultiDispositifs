#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

class Groupe:
    """
    A class to represent a group
    """

    def __init__(self, identifier):
        """
        Initialize the group
        :param identifier: the identifier of the group
        """
        self.identifier = identifier
        self.users = []

    def add_user(self, user):
        """
        Add an user to the group
        :param user: the user to add
        """
        self.users.append(user)

    def get_user(self, identifier):
        """
        Get a specific user of the group
        :param identifier: the identifier of the user
        """
        for user in self.users:
            if user.identifier == identifier:
                return user
        return None

    def get_color(self, identifier):
        """
        Get the color of an user
        :param identifier: user's identifier
        :return: the color of the specified user
        """
        for user in self.users:
            if user.identifier == identifier:
                tmp = user.color
                return user.color + [1]
        return None

    def nb_users(self):
        """
        Get the number of users in the group
        :return: the number of users in the group
        """
        return len(self.users)

    def nb_criterions(self):
        """
        Get the number of criterions in the group
        :return: the number of criterions in the group
        """
        cpt = 0
        for user in self.users:
            cpt += user.nb_criterions
        return cpt

    def nb_links_persos(self):
        """
        Get the number of personal links in the group
        :return: the number of personal links in the group
        """
        cpt = 0
        for user in self.users:
            cpt += user.nb_links_persos
        return cpt

    def nb_links_others(self):
        """
        Get the number of collaborative links in the group
        :return: the number of collaborative links in the group
        """
        cpt = 0
        for user in self.users:
            cpt += user.nb_links_others
        return cpt
