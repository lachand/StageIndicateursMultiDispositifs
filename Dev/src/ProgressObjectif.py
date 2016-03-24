#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget


class ProgressObjectif(Widget):
    """
    A class to represent the indicator representing the progress comparing to objectives
    """

    def __init__(self, objective, position, level_max):
        """
        Initialize the indicator
        :param objective: a table of different objectives
        :param position: the position of the indicator
        :param level_max: the max number of objectives
        """
        Widget.__init__(self)
        self.objective = objective
        self.progress = 0
        self.level = 0
        self.level_max = level_max

        btn_new_image = Button(text='news images', size=[200, 50])
        btn_new_image.pos = (position[0] - btn_new_image.width / 2, position[1])
        btn_new_image.bind(on_press=self.callback)

        self.pb = ProgressBar(max=self.objective, value=self.progress, size=[200, 0])
        self.pb.pos = (position[0] - self.pb.width / 2, position[1] + btn_new_image.height)
        self.add_widget(btn_new_image)
        self.add_widget(self.pb)

    def update(self):
        """
        Update the indicator when criterions are created
        """
        self.progress = len(self.parent.criterions)
        self.pb.value = self.progress

    def callback(self, value):
        """
        Add new animals to the table if the current objective is done
        """
        if self.progress >= self.objective and self.level < self.level_max:
            table = self.parent
            table.current_lvl += 1
            self.level += 1
            self.objective = self.parent.news_images(self.level)
            self.pb.max = self.objective
