from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from random import randint
from ZoneUtilisateur import ZoneUtilisateur
from kivy.uix.colorpicker import Color
from kivy.graphics import Rectangle


class Animal(Scatter):
    def __init__(self, id, image, pos):
        self.couleur = [0, 0, 0]
        Scatter.__init__(self)
        self.src_image = image
        self.image = Image(source=image)
        self.taille = self.image.size
        self.center = [randint(200, pos[0]), randint(200, pos[1])]
        self.identifiant = id
        self.current_utilisateur = None
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(source=self.src_image, size=[self.taille[0] - 10, self.taille[1] - 10])

    def set_utilisateur(self, utilisateur):
        self.current_utilisateur = utilisateur
        self.couleur = utilisateur.couleur
        self.canvas.clear()
        with self.canvas:
            Color(self.couleur[0], self.couleur[1], self.couleur[2])
            Rectangle()
            Color(1, 1, 1, 1)
            Rectangle(source=self.src_image, size=[self.taille[0] - 10, self.taille[1] - 10])

    def remove_utilisateur(self):
        self.current_utilisateur = None
        self.couleur = [1, 1, 1]
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(source=self.src_image, size=[self.taille[0] - 10, self.taille[1] - 10])

    def update(self, dt):
        for child in self.parent.children:
            if child.__class__ == ZoneUtilisateur and child.collide_point(self.center[0], self.center[1]):
                if self.current_utilisateur is None:
                    self.set_utilisateur(child.utilisateur)
