#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


class Choix(Widget):
    """
    Class representing the choice window
    """

    def __init__(self,size):
        """
        Initialize the window
        :param size: size of the window
        """
        Widget.__init__(self)
        self.qui = CheckBox(pos=(size[0]/2- 300, size[1] - 100) ,group="choix", text='Qui :')
        self.label_qui = Label(text='Qui ?', font_size=40, pos=(size[0]/2-240, size[1] - 100))
        self.quoi = CheckBox(pos=(size[0]/2-180, size[1] - 100) ,group="choix", text='Quoi :')
        self.label_quoi = Label(text='Quoi ?', font_size=40, pos=(size[0]/2-100, size[1] - 100))
        self.quand = CheckBox(pos=(size[0]/2-30, size[1] - 100) ,group="choix", text='Quand :')
        self.label_quand = Label(text='Quand ?', font_size=40, pos=(size[0]/2+60, size[1] - 100))
        self.ou = CheckBox(pos=(size[0]/2+150, size[1] - 100) ,group="choix", text='Ou :')
        self.label_ou = Label(text='Ou ?', font_size=40, pos=(size[0]/2+210, size[1] - 100))
        self.comment = CheckBox(pos=(size[0]/2- 300, size[1] - 150) ,group="choix", text='Comment :')
        self.label_comment = Label(text='Comment ?', font_size=40, pos=(size[0]/2-180, size[1] - 150))
        self.pourquoi = CheckBox(pos=(size[0]/2- 30, size[1] - 150) ,group="choix", text='Pourquoi :')
        self.label_pourquoi = Label(text='Pourquoi ?', font_size=40, pos=(size[0]/2-30+120, size[1] - 150))
        self.btn_validate = Button(text='Valider', font_size=40, size=(300, 80), pos=(size[0]/2- 350, 100))
        self.btn_suppress = Button(text='Supprimer', font_size=40, size=(300, 80), pos=(size[0] / 2 + 50, 100))
        self.btn_validate.bind(on_press=self.callback)
        self.btn_suppress.bind(on_press=self.callback_destroy)
        self.add_widget(self.qui)
        self.add_widget(self.label_qui)
        self.add_widget(self.quoi)
        self.add_widget(self.label_quoi)
        self.add_widget(self.quand)
        self.add_widget(self.label_quand)
        self.add_widget(self.ou)
        self.add_widget(self.label_ou)
        self.add_widget(self.comment)
        self.add_widget(self.label_comment)
        self.add_widget(self.pourquoi)
        self.add_widget(self.label_pourquoi)
        self.add_widget(self.btn_validate)
        self.add_widget(self.btn_suppress)

        self.popup = Popup(title='Action requise :', title_size=40,
                           content=Label(text='Merci de choisir une catégorie',
                                         font_size=40), size=(600, 400), size_hint=(None, None))

    def callback_destroy(self, value):
        """"
        Go back to the main menu
        """
        self.parent.main_menu()

    def callback(self, value):
        """
        Set the question type for the creation of criterion
        """
        active = None
        if self.qui.active :
            active = "Qui :"
        elif self.quoi.active :
            active = "Quoi :"
        elif self.quand.active :
            active = "Quand :"
        elif self.comment.active :
            active = "Comment :"
        elif self.ou.active :
            active = "Ou :"
        elif  self.pourquoi.active :
            active = "Pourquoi :"

        if active is not None :
            self.parent.clavier.validate(active)
            self.parent.main_menu()

        else:
            self.popup.open()