from kivy.uix.widget import Widget
from Critere import Critere
from Animal import Animal
from Utilisateur import Utilisateur
from kivy.uix.colorpicker import Color
from kivy.graphics import Line

class Links(Widget):

    def update(self, dt):
        self.canvas.clear()
        for child in self.parent.children:
            if child.__class__ == Critere :
                for lien in child.Links:
                    for child2 in self.parent.children:
                        if child2.__class__ == Animal and lien[0] == child2.getID() :
                            utilisateur = self.parent.getUtilisateur(lien[1])
                            with self.canvas:
                                couleur = utilisateur.getCouleur()
                                Color(couleur[0],couleur[1],couleur[2])
                                Line(points=[child.center[0],child.center[1],child2.center[0],child2.center[1]],width=2)