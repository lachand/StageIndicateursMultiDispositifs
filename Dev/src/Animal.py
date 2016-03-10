from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from random import randint
from ZoneUtilisateur import ZoneUtilisateur
from kivy.uix.colorpicker import Color
from kivy.graphics import Rectangle


class Animal(Scatter):
    def __init__(self, id, image, pos):
        self.Couleur = [0, 0, 0]
        Scatter.__init__(self)
        self.srcImage = image
        self.Image = Image(source=image)
        self.Taille = self.Image.size
        self.center = [randint(200, pos[0]), randint(200, pos[1])]
        self.ID = id
        self.Current_utilisateur = None
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(source=self.srcImage, size=[self.Taille[0] - 10, self.Taille[1] - 10])

    def setUtilisateur(self, utilisateur):
        self.Current_utilisateur = utilisateur
        self.Couleur = utilisateur.getcouleur()
        self.canvas.clear()
        with self.canvas:
            Color(self.Couleur[0], self.Couleur[1], self.Couleur[2])
            Rectangle()
            Color(1, 1, 1, 1)
            Rectangle(source=self.srcImage, size=[self.Taille[0] - 10, self.Taille[1] - 10])

    def removeUtilisateur(self):
        self.Current_utilisateur = None
        self.Couleur = [1, 1, 1]
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(source=self.srcImage, size=[self.Taille[0] - 10, self.Taille[1] - 10])

    def getUtilisateur(self):
        return self.Current_utilisateur

    def getid(self):
        return self.ID

    def update(self, dt):
        for child in self.parent.children:
            if child.__class__ == ZoneUtilisateur and child.collide_point(self.center[0], self.center[1]):
                if self.Current_utilisateur is None:
                    self.setUtilisateur(child.getUtilisateur())
