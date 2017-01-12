#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import json
import os
import urllib2
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from Animal import Animal
from Configuration import Configuration
from Critere import Critere
from Dev.src.libs.backend.backendweb import BackendWeb
from Groupe import Groupe
from TableApp import TableApp
from IndicateurCritere import IndicateurCritere
from IndicateurVote import IndicateurVote
from Links import Links
from Logger import Logger
from ProgressObjectif import ProgressObjectif
from Serveur import Serveur
Builder.load_file(os.path.join(os.path.dirname(__file__),'template.kv'))

Config.set('kivy', 'keyboard_mode', 'multi')
#Config.set('kivy', 'keyboard_layout', 'keyboard.json')
Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '700')
Config.set('graphics','fullscreen','1')

PATH = os.path.join("..", "cfg", "ConfigExpeIntegre.json")


class Table(Widget):    """
    A class to represent a table
    """

    def __init__(self, **kwargs):
        """
        Initialize the table
        """
        super(Table, self).__init__(**kwargs)
        self.configuration = Configuration(PATH)
        self.logger = Logger()
        ipport = self.configuration.server_infos()
        self.server = Serveur(self,ipport[0],ipport[1])
        self.has_internet = self.internet_on()
        if self.has_internet:
            self.backend = BackendWeb(
                url="http://museotouch.fr/api/interface_v2/",
                data_url="http://museotouch.fr/api/interface_v2/",
                decode=False)
        self.layout = GridLayout(cols=10, size=self.size)
        self.menu_mode = True
        self.image_user = Image(source="Images/user.png")
        self.image_user_yes = Image(source="Images/user_validate.png")
        self.image_user_no = Image(source="Images/user_unvalidate.png")

    def internet_on(self):
        """
        Check the internet connection
        :return: if the internet connection is on or not
        """
        try:
            urllib2.urlopen('http://museotouch.fr',timeout=5)
            return True
        except urllib2.URLError as err:
            return False

    def update_vote(self):
        """
        Update votes for the vote's indicator
        :return:
        """
        for fils in self.children:
            if fils.__class__ == IndicateurVote :
                fils.update()

    def initialisation(self, size):
        """
        Initialize the table
        :param size: the size of the screen
        """
        self.user = []
        self.connected = []
        self.animals = []
        self.criterions = []
        self.images_folder = []
        self.objective_criterions = []
        self.current_lvl = 0
        self.integrated_links = None
        self.integrated_criterions = None
        self.vote_integrated = None
        self.progress_objective = []
        self.group = Groupe(1)
        self.indicators = []
        self.user_zones = []
        self.widget_to_add = []

        from kivy.uix.button import Button
        self.size = size.size
        self.layout.size = self.size

        if self.has_internet:

            self.backend.get_expos(uid=7970)

            result = self.backend.req.result
            with open("tmp.json", 'w') as fd:
                from json import dump
                dump([result], fd)
                fd.close()
            with open("tmp.json", "r") as fd:
                json_data = fd.read()
                data = json.loads(json_data)
            for elmt in data[0]["items"]:
                btn = Button(text=elmt["fields"]["Nom"])
                btn.bind(on_press=self.config)
                self.layout.add_widget(btn)

        else:
            for root, dirs, files in os.walk("../Activities"):
                for name in files:
                    if name == "config.json":
                        with open(root+"/config.json", "r") as fd:
                            json_data = fd.read()
                            data = json.loads(json_data)
                            btn = Button(text=data["name"])
                            btn.bind(on_press=self.config)
                            self.layout.add_widget(btn)
        self.add_widget(self.layout)

    def get_zone_utilisateur(self, user):
        """
        Get the zone corresponding to a specified user
        :param user: the user to get the zone
        :return: the thone of the user
        """
        for zone in self.user_zones:
            if zone.user == user :
                return zone
        return None

    def config(self, id):
        """
        Configure the application with the correct activity
        :param id: the name of the activity
        :return:
        """
        self.menu_mode = False
        if self.has_internet:
            with open("tmp.json", "r") as fd:
                json_data = fd.read()
                data = json.loads(json_data)
            for elmt in data[0]["items"]:
                if elmt["fields"]["Nom"] == id.text:
                    identifier = int(elmt["fields"]["id"])
        else:
            for root, dirs, files in os.walk("../Activities"):
                for name in files:
                    if name == "config.json":
                        with open(root+"/config.json", "r") as fd:
                            json_data = fd.read()
                            data = json.loads(json_data)
                            if data["name"] == id.text:
                                identifier = data["id"]

        self.configuration.config_table(self,identifier)
        links = Links(self.integrated_links)
        self.add_widget(links)
        links.draw_label()

    def remove_user(self,user):
        """
        Remove a specified user
        :param user: the user to remove
        """
        self.connected.remove(user.identifier)
        for zone in self.user_zones:
            if zone.user == user:
                zone.set_name("")
                zone.connected = False

    def add_criterion(self, criterion):
        """
        Add a criterion to the table
        :param criterion: the criterion to add
        """
        self.add_widget(criterion)
        criterion.draw()
        self.criterions.append(criterion)
        self.logger.write("create_critere", criterion.createur.identifier, [1,criterion.texte])
        for child in self.children:
            if child.__class__ == ProgressObjectif or child.__class__ == IndicateurCritere:
                child.update()

    def new_criterion(self, text, user,fusionneurs=[],text_type=""):
        """
        Create a new criterion
        :param text: text of the criterion
        :param user: creator of the criterion
        :param fusionneurs: editors of the criterion
        :param text_type: question's type
        :return:
        """
        identifier = self.free_criterion_id()
        if user.identifier == 2 or user.identifier == 3:
            criterion = Critere(identifier, text, user, (user.position[0],user.position[1]-100), self.integrated_criterions, "table", fusionneurs = fusionneurs, text_type=text_type)
        else:
            criterion = Critere(identifier, text, user, (user.position[0], user.position[1]),
                            self.integrated_criterions, "table", fusionneurs=fusionneurs, text_type=text_type)
        self.criterions.append(criterion)

        self.logger.write("edit_critere", criterion.createur.identifier, [1, criterion.texte])
        self.add_widget(criterion)

        for child in self.children:
            if child.__class__ == ProgressObjectif or child.__class__ == IndicateurCritere:
                child.update()

        return criterion

    def get_animal(self, identifier):
        """
        Get a specified animal
        :param identifier: identifier of the animal
        :return: the specified animal
        """
        for child in self.children:
            if child.__class__ == Animal and child.identifier == identifier:
                return child
        return None

    def free_criterion_id(self):
        """
        Check the first free criterion identifier
        :return: the first free criterion identifier
        """
        tab = []
        for criterion in self.criterions:
            tab.append(criterion.identifier)
        tab.sort()
        for i in range(0, len(tab) - 1):
            if tab[i] != i + 1:
                return i + 1
        return len(tab)

    def news_images(self, level):
        """
        Add images of a level to the table
        :param level: the level of the images
        """
        #self.add_animal_lvl(level)
        return self.objective_criterions[self.current_lvl]

    def add_animal_lvl(self, lvl):
        """
        Add images of a level to the table
        :param lvl: the level of the images
        """
        r1 = self.get_root_window().width - 200
        r2 = self.get_root_window().height - 200
        # images = glob.glob(self.images_folder[lvl])
        # for images in images:
        #    self.add_animal(len(self.animals) + 1, images, [r1, r2])
        for image in self.images_folder[lvl]:
            self.add_animal(len(self.animals) + 1, image, [r1, r2], lvl)

    def lock_animal(self, lvl):
        """
        Lock all animal of a level
        :param lvl: the level to lock
        """
        for child in self.children:
            if child.__class__ == Animal :
                if child.lvl == lvl :
                    child.lock()

    def unlock_animal(self, lvl):
        """
        Unlock all animal of a level
        :param lvl: the level to unlock
        """
        for child in self.children:
            if child.__class__ == Animal :
                if child.lvl == lvl :
                    child.unlock()

    def update_animal(self, lvl, value):
        """
        Change opacity of images
        :param lvl: the level to change opacity
        :param value: the new value of the opacity
        :return:
        """
        for child in self.children:
            if child.__class__ == Animal :
                if child.lvl == lvl :
                    child.set_opacity(value)

    def add_animal(self, identifier, image, pos, lvl):
        """
        Add an animal to the table
        :param identifier: the identifier of the animal
        :param image: the source of the image representing the animal
        :param pos: the position where to add the animal
        """
        animal = Animal(identifier, image, pos, self, "table", lvl)
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
        :param dt:
        """
        # from PhysicalIndicator import PhysicalIndicator
        for elmt in self.widget_to_add:
            self.add_widget(elmt)
            self.widget_to_add.remove(elmt)
        for child in self.children:
            if child.__class__ == Critere or child.__class__ == Links: # or child.__class__ == IndicateurVote:  # or child.__class__ == PhysicalIndicator:
                child.update(dt)

    def get_user(self, identifier):
        """
        Get a specific user of the table
        :param identifier: the identifier of the user to ger
        :return: the user needed
        """
        return self.group.get_user(identifier)

    def connect_user(self, newsock):
        """
        Connect an user
        :param newsock: the socket of the user
        :return: the user
        """
        if len(self.connected) == 0:
            self.connected.append(self.group.users[0].identifier)
            self.group.users[0].add_socket(newsock)
            return self.group.users[0]
        else:
            for user in self.group.users:
                if self.connected.count(user.identifier) == 0:
                    self.connected.append(user.identifier)
                    user.add_socket(newsock)
                    return user
        return None

    def menu(self):
        """
        Go back to the main menu
        """
        for fils in self.children :
            self.remove_widget(fils)
        self.initialisation(self.size)

if __name__ == '__main__':
    app = TableApp()
    app.run()



