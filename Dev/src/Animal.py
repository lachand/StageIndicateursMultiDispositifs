from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from random import randint
from ZoneUtilisateur import ZoneUtilisateur
from kivy.uix.colorpicker import Color
from kivy.graphics import Rectangle


class Animal(Scatter):
    """
    A Class representing an animal
    """
    def __init__(self, id, image, pos):
        """
        Initialize an animal
        :param id: the id of the animal
        :param image: the path of the image for the animal
        :param pos: the square where the scater can be randomly placed
        """
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
        """
        Set the current user of the animal
        :param utilisateur: the user that is using the animal
        """
        self.current_utilisateur = utilisateur
        self.couleur = utilisateur.couleur
        self.canvas.clear()
        with self.canvas:
            Color(self.couleur[0], self.couleur[1], self.couleur[2])
            Rectangle()
            Color(1, 1, 1, 1)
            Rectangle(source=self.src_image, size=[self.taille[0] - 10, self.taille[1] - 10])

    def remove_utilisateur(self):
        """
         Remove the current user of the animal
         """
        self.current_utilisateur = None
        self.couleur = [1, 1, 1]
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(source=self.src_image, size=[self.taille[0] - 10, self.taille[1] - 10])

    def update(self, dt):
        """
        Create link between the animal and a concept the animal is used by someone and collid with a concept
        """
        for child in self.parent.children:
            if child.__class__ == ZoneUtilisateur and child.collide_point(self.center[0], self.center[1]):
                if self.current_utilisateur is None:
                    self.set_utilisateur(child.utilisateur)
