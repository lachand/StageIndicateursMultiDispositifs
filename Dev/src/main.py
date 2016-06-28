#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = '1.0'

import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.colorpicker import Color
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from Animal import Animal
from Choix import Choix
from Clavier import Clavier
from Client import Client
from Critere import Critere
from Groupe import Groupe
from Links import Links
from Logger import Logger
from Utilisateur import Utilisateur

Builder.load_file('template.kv')


class Tablette(Widget):
    current_lvl = 0
    colored_links = True
    integrated_criterions = True
    logger = Logger()
    name = ''

    def __init__(self, parent):
        Widget.__init__(self)
        self.group = Groupe(1)
        self.identifier = 0
        self.widget_connection = []
        self.parent = parent
        self.user = None
        self.TrueColor = [0, 0, 0]
        self.to_load = []
        self.criterions = []
        self.indicators = []
        self.add_widget(Links(self.colored_links))
        self.edition_mode=False
        self.image_user = Image(source="Images/user.png")

    def get_user(self, identifier):
        return self.group.get_user(identifier)

    def set_user(self, identifier, color):
        self.user = Utilisateur(identifier, color, 3, [0, 50])

    def add_criterion(self, criterion):
        self.add_widget(criterion)
        criterion.draw()
        self.criterions.append(criterion)

    def callback(self, value):
        if not self.edition_mode:
            self.edition_mode = True
            self.remove_widget(self.button)
            self.remove_widget(self.lab)
            self.choix = Choix(self.size)
            self.add_widget(self.choix)

            self.clavier = Clavier(self.user, self.user.color, (0, 170), 0, "tablette", (self.width, self.height))
            self.add_widget(self.clavier)
            self.clavier.initialisation()

    def main_menu(self):
        self.remove_widget(self.choix)
        self.clavier.destroy()
        self.add_widget(self.button)
        self.add_widget(self.lab)

    def set_color(self, color):
        self.size = self.get_root_window().size
        self.TrueColor = color
        with self.canvas:
            Color(color[0], color[1], color[2], 1)
            Rectangle(pos=(0, self.height - 160), size=(self.width, 160))
            Color(1, 1, 1, 1)
        self.lab = Label(text='Déplacer ici pour envoyer', font_size=40, pos=(0, self.height - 160), size=(self.width, 160),valign='top',halign='center')
        self.add_widget(self.lab)

    def set_identifier(self, identifier):
        self.identifier = identifier

    def ask_server_adress(self, root):
        self.size = root.size
        label_ip = Label(text='IP serveur :', font_size=40, size=(400, 80),
                         pos=(self.width / 2 - 200, self.height / 2 + 200))
        ti_ip = TextInput(text="10.42.0.1", font_size=40, size=(400, 60),
                          pos=(self.width / 2 - 200, self.height / 2 + 140), on_text_validate=self.initialisation, multiline = False)
        label_port = Label(text='Port serveur :', font_size=40, size=(400, 80),
                           pos=(self.width / 2 - 200, self.height / 2 + 60))
        ti_port = TextInput(text='8080', font_size=40, size=(400, 60), pos=(self.width / 2 - 200, self.height / 2), on_text_validate=self.initialisation, multiline = False)
        label_name = Label(text='Prénom :', font_size=40,size=(400, 80),
                           pos=(self.width / 2 - 200, self.height / 2 + -80))
        self.ti_name = TextInput(text='', font_size=40, size=(400, 60), pos=(self.width / 2 - 200, self.height / 2 - 140), on_text_validate=self.initialisation, multiline = False)
        button = Button(text='Connexion', font_size=40, size=(400, 100),
                        pos=(self.width / 2 - 200, self.height / 2 - 280))
        self.add_widget(ti_ip)
        self.add_widget(ti_port)
        self.add_widget(self.ti_name)
        self.add_widget(label_ip)
        self.add_widget(label_port)
        self.add_widget(label_name)
        self.add_widget(button)

        self.widget_connection.append(ti_ip)
        self.widget_connection.append(ti_port)
        self.widget_connection.append(label_ip)
        self.widget_connection.append(label_port)
        self.widget_connection.append(button)
        self.widget_connection.append(label_name)
        self.widget_connection.append(self.ti_name)

        self.popup = Popup(title='Action requise :', title_size = 40,
                           content=Label(text='Merci de rentrer votre prénom',
                           font_size=40),size=(600,400),size_hint=(None,None))

        button.bind(on_press=self.initialisation)

    def initialisation(self, value):
        if len(self.ti_name.text) > 0:
            self.name = self.ti_name.text
            self.client = Client(self, self.widget_connection[0].text, self.widget_connection[1].text)

            for widget in self.widget_connection:
                self.remove_widget(widget)

            self.button = Button(text='Nouvelle reponse', font_size=40, size=(800, 80), pos=(self.width / 2 - 400, 100))
            self.button.bind(on_press=self.callback)
            self.add_widget(self.button)

            t1 = threading.Thread(target=self.client.run_client)
            t1.daemon = True
            t1.start()
        else:
            self.popup.open()

    def new_criterion(self, text, user):
        criterion = Critere(1, text, user, (self.width / 2, self.height - 100), True, "tablette")
        self.criterions.append(criterion)
        self.add_widget(criterion)
        criterion.draw()
        return criterion

    def edit_criterion(self,text,user,fusionneurs=[],text_type=""):
        criterion = Critere(1, text, user, (self.width / 2, self.height - 100), True, "tablette",fusionneurs=fusionneurs,text_type=text_type)
        self.add_widget(criterion)
        if not self.edition_mode:
            self.edition_mode = True
            self.remove_widget(self.button)
            self.remove_widget(self.lab)
            self.choix = Choix(self.size)
            self.add_widget(self.choix)

            self.clavier = Clavier(self.user, self.user.color, (0, 170), 0, "tablette", (self.width, self.height), criterion, text_type=text_type)
            self.add_widget(self.clavier)
            self.clavier.initialisation()
        else :
            criterion.send_to_table()



    def add_animal(self, src_img, identifier):
        here = False
        for child in self.children:
            if child.__class__ == Animal and child.identifier == identifier:
                here = True
        if not here:
            self.to_load.append((src_img, identifier))

    def remove_animal(self, identifier):
        for child in self.children:
            if child.__class__ == Animal and child.identifier == identifier:
                child.canvas.clear()
                self.remove_widget(child)

    def update(self, dt):
        tmp = set(self.to_load)
        self.to_load = list(tmp)

        for child in self.children:
            if child.__class__ == Critere :
                child.update(dt)

    def get_user(self, identifier):
        return self.group.get_user(identifier)

    def add_user(self, identifier, color):
        user = Utilisateur(identifier, color)
        self.group.add_user(user)


class TabletteclientApp(App):
    tablette = None

    def build(self):
        self.tablette = Tablette(self)
        Clock.schedule_interval(self.tablette.update, 1.0 / 60.0)
        return self.tablette

    def on_start(self):
        self.tablette.ask_server_adress(self.root_window)

    def on_stop(self):
        self.tablette.client.on_stop()


if __name__ == '__main__':
    app = TabletteclientApp()
    app.run()
