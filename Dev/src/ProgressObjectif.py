#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.colorpicker import Color
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

        self.btn_new_image = Button(text='news images', size=[200, 50])
        self.btn_new_image.pos = (position[0] - self.btn_new_image.width / 2, position[1])
        self.btn_new_image.bind(on_press=self.callback)

        #self.pb = ProgressBar(max=self.objective, value=self.progress, size=[200, 0])
        self.pos_progress_bar = (position[0] - self.btn_new_image.width / 2, position[1] + self.btn_new_image.height)
        self.add_widget(self.btn_new_image)
        #self.add_widget(self.pb)

    def update(self, dt):
        """
        Update the indicator when criterions are created
        """
        users = [0]*len(self.parent.group.users)
        sum = 0
        for criterion in self.parent.criterions:
            users[criterion.createur.identifier-1] += 1
            sum += 1
        with self.canvas:
            Color(255, 255, 255, .75)
            Rectangle(pos=self.pos_progress_bar,size=(self.btn_new_image.width-1,20))
            if sum <= self.parent.objective_criterions[self.parent.current_lvl]:
                step = self.btn_new_image.width/self.parent.objective_criterions[self.parent.current_lvl] +1
            else:
                step = self.btn_new_image.width/sum
            cpt = 0
            for i in range(1,len(users)+1):
                user = self.parent.get_user(i)
                Color(user.color[0], user.color[1], user.color[2], 1)
                Rectangle(pos=(self.pos_progress_bar[0]+cpt*step,self.pos_progress_bar[1]),size=(users[i-1]*step,20))
                cpt+= users[i-1]

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
