#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.uix.widget import Widget

from Vote import Vote


class ZoneVote(Widget):
    """
    A class to represent the vote's zone
    """
    def __init__(self, user, pos, angle):
        """
        Initialize the indicator
        :param user: the user of which the indicator is about
        :param pos: the position of the indicator
        """
        self.user = user
        self.position = pos
        print pos
        self.color = self.user.color
        self.angle = angle
        Widget.__init__(self)
        self.add_widget(Vote(self.user.identifier, 1, pos, angle, self.user))
        self.add_widget(Vote(self.user.identifier, 0, pos, angle, self.user))
