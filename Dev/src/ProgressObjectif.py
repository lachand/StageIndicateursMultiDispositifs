#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.colorpicker import Color
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget


class ProgressObjectif(Widget):
    """
    A class to represent the indicator representing the progress comparing to objectives
    """

    def __init__(self, objective, position, level_max, integrated=True, url=None):
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
        self.countdown = objective
        self.level_max = level_max
        self.integrated = integrated
        self.position = position
        self.url = url

        btn_new_image = Button(text="Ajout d'images", size=[200, 50])
        btn_new_image.pos = (position[0] - btn_new_image.width / 2, position[1])
        btn_new_image.bind(on_press=self.callback)

        if not self.integrated:
            self.pb = ProgressBar(max=self.objective, value=self.progress, size=[200, 0])
            self.pb2 = ProgressBar(max=self.objective, value=self.progress, size=[200, 0])
            self.pb3 = ProgressBar(max=self.objective, value=self.progress, size=[200, 0])
            self.pb.pos = (position[0] - self.pb.width / 2, position[1] + btn_new_image.height)
            self.pb2.pos = (position[0] - self.pb.width / 2, position[1] + btn_new_image.height + 2)
            self.pb3.pos = (position[0] - self.pb.width / 2, position[1] + btn_new_image.height + 5)
        elif self.integrated and self.countdown >= 0:
            from kivy.uix.image import Image
            from kivy.loader import Loader
            proxyImage = Loader.image(str(self.url))
            proxyImage.bind(on_load=self._image_loaded)
            self.pb = Image()
            self.pb.pos = (position[0] - self.pb.width / 2, position[1] + btn_new_image.height)
            self.position = (position[0] - self.pb.width / 2, position[1] + btn_new_image.height)
            with self.canvas:
                Color(1, 1, 1, 1)
                Rectangle(texture=self.pb.texture,
                          size=(self.pb.width, self.pb.height * (1 - (float(self.progress) / float(self.objective)))),
                          pos=(
                              self.position[0], self.position[1] + self.pb.height * (self.progress / self.objective)))
                Color(0, 0, 0, 1)
                Rectangle(size=(self.pb.width, self.pb.height * (1 - (float(self.progress) / float(self.objective)))),
                          pos=self.pb.pos)

        self.add_widget(btn_new_image)
        if not self.integrated:
            self.add_widget(self.pb)
            self.add_widget(self.pb2)
            self.add_widget(self.pb3)

    def _image_loaded(self, proxyImage):
        if proxyImage.image.texture:
            self.pb.texture = proxyImage.image.texture

    def update(self):
        """
        Update the indicator when criterions are created
        """
        self.progress = len(self.parent.criterions)
        self.parent.logger.write("update_objective", "all", [self.level, self.progress, self.objective])
        self.pb.value = self.progress
        self.countdown = self.objective - self.progress
        if not self.integrated:
            self.pb2.value = self.progress
            self.pb3.value = self.progress
        if self.integrated and self.countdown >= 0:
            self.parent.update_animal(self.level+1, float(self.progress)/float(self.objective))
        if self.integrated and self.countdown < 0:
            with self.canvas:
                Color(0, 0, 0)
                Rectangle(size=(self.pb.width, self.pb.height * (1 - (float(self.progress) / float(self.objective)))),
                          pos=(self.pb.pos[0], self.pb.pos[1]))

    def callback(self, value):
        """
        Add new animals to the table if the current objective is done
        :param value:
        """
        if self.progress >= self.objective and self.level < self.level_max:
            table = self.parent
            table.current_lvl += 1
            self.level += 1
            self.objective = table.news_images(self.level)
            self.countdown = self.objective - self.progress
            if not self.integrated:
                self.pb.max = self.objective
                self.pb2.max = self.objective
                self.pb3.max = self.objective
            table.unlock_animal(self.level)