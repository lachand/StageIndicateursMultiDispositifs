from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from random import randint
from ZoneUtilisateur import ZoneUtilisateur
from kivy.uix.colorpicker import Color
from kivy.graphics import Rectangle
from shapely.geometry import Polygon
from math import sin, cos, pi


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
        self.on_move = False
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

    def on_touch_move(self, touch):
        """
        Update the distance and angle between the animal and each of his links and set the user touching the animal
        :param touch: the position of the touch
        """
        if self.collide_point(touch.x, touch.y) :
            for critere in self.parent.criteres:
                value = critere.has_link(self.identifiant)
                if value != -1:
                    critere.update_link(value,self.center)

            for child in self.parent.children:
                if child.__class__ == ZoneUtilisateur and child.collide_point(self.center[0], self.center[1]):
                    if self.current_utilisateur is None:
                        self.set_utilisateur(child.utilisateur)
            Scatter.on_touch_move(self, touch)

    def update_coordinate(self,x,y):
        points = []
        for critere in self.parent.criteres :
            for lien in critere.links:
                if lien.linked_to_animal(self.identifiant):
                    x = critere.center_x + lien.distance*cos(lien.angle+pi)
                    y = critere.center_y + lien.distance*sin(-lien.angle+pi)
                    points.append([x,y])
        if len(points) == 1 :
            if x > 0 and x < self.parent.size[0]:
                self.center_x = x
            if y > 0 and y < self.parent.size[1]:
                self.center_y = y
        elif len(points) == 2 :
            x = (points[0][0] + points[1][0])/2
            y = (points[0][1] + points[1][1])/2
            if x > 0 and x < self.parent.size[0]:
                self.center_x = x
            if y > 0 and y < self.parent.size[1]:
                self.center_y = y
        elif len(points) > 2 :
            poly = Polygon(points)
            point = poly.centroid
            if x > 0 and x < self.parent.size[0]:
                self.center_x = point.x
            if y > 0 and y < self.parent.size[1]:
                self.center_y = point.y