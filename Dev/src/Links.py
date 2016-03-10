from kivy.uix.widget import Widget
from Critere import Critere
from Animal import Animal
from kivy.uix.colorpicker import Color
from kivy.graphics import Line


class Links(Widget):
    def __init__(self, colored):
        self.Colored = colored
        Widget.__init__(self)

    def update(self, dt):
        self.canvas.clear()
        for child in self.parent.children:
            if child.__class__ == Critere:
                for lien in child.Links:
                    for child2 in self.parent.children:
                        if child2.__class__ == Animal and lien[0] == child2.getid():
                            utilisateur = self.parent.getUtilisateur(lien[1])
                            with self.canvas:
                                if self.Colored:
                                    couleur = utilisateur.getcouleur()
                                    Color(couleur[0], couleur[1], couleur[2])
                                else:
                                    Color(.25, .25, .25)
                                Line(points=[child.center[0], child.center[1], child2.center[0], child2.center[1]],
                                     width=2)
