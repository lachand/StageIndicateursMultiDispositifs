#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import glob

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.widget import Widget

from Animal import Animal
from Configuration import Configuration
from Critere import Critere
from GenerateurRapport import GenerateurRapport
from Groupe import Groupe
from Links import Links
from ProgressObjectif import ProgressObjectif
import os

Builder.load_file('template.kv')

Config.set('kivy', 'keyboard_mode', 'multi')
Config.set('kivy', 'keyboard_layout', 'keyboard.json')
Config.set('graphics', 'fullscreen', 'auto')

PATH = os.path.join("..", "cfg", "ConfigSimple.json")


class Table(Widget):
    """
    A class to represent a table
    """
    user = []
    animals = []
    criterions = []
    images_folder = []
    objective_criterions = []
    current_lvl = 0
    colored_links = True
    colored_criterions = True
    progress_objective = []
    group = Groupe(1)

    def initialisation(self, size):
        """
        Initialize the table
        :param size: the size of the screen
        """
        configuration = Configuration(PATH)
        self.size = size.size
        configuration.config_table(self)
        self.add_widget(Links(self.colored_links))

    def add_criterion(self, criterion):
        """
        Add a criterion to the table
        :param criterion: the criterion to add
        """
        self.add_widget(criterion)
        self.criterions.append(criterion)
        for child in self.children:
            if child.__class__ == ProgressObjectif:
                child.update()

    def news_images(self, level):
        """
        Add images of a level to the table
        :param level: the level of the images
        """
        self.add_animal_lvl(level)
        return self.objective_criterions[self.current_lvl]

    def add_animal_lvl(self, lvl):
        """
        Add images of a level to the table
        :param lvl: the level of the images
        """
        r1 = self.get_root_window().width - 200
        r2 = self.get_root_window().height - 200
        images = glob.glob(self.images_folder[lvl])
        for images in images:
            self.add_animal(len(self.animals) + 1, images, [r1, r2])

    def add_animal(self, identifier, image, pos):
        """
        Add an animal to the table
        :param identifier: the identifier of the animal
        :param image: the source of the image representing the animal
        :param pos: the position where to add the animal
        """
        animal = Animal(identifier, image, pos)
        self.animals.append(identifier)
        self.add_widget(animal)

    def add_indicateur(self, indicateur):
        """
        Add an indicator to the table
        :param indicateur: the indicator to add
        """
        self.add_widget(indicateur)

    def update(self, dt):
        """
        Update the table
        """
        for child in self.children:
            if child.__class__ == Critere or child.__class__ == Links:
                child.update(dt)

    def get_user(self, identifier):
        """
        Get a specific user of the table
        :param identifier: the identifier of the user to ger
        :return: the user needed
        """
        return self.group.get_user(identifier)


class TableApp(App):
    def build(self):
        self.table = Table()
        Clock.schedule_interval(self.table.update, 1.0 / 60.0)
        return self.table

    def on_start(self):
        self.table.initialisation(self.root_window)

    def on_stop(self):
        configuration = Configuration(PATH)
        generateur = GenerateurRapport()
        configuration.config_generateur(generateur)
        generateur.generation(self.table)


if __name__ == '__main__':
    TableApp().run()
