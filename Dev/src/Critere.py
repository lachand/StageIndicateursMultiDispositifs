from kivy.graphics import Ellipse
from kivy.uix.colorpicker import Color
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from Link import Link
import math


class Critere(Scatter):
    """
    A class to represent a criterion
    """
    def __init__(self, id, texte, createur, position, colored):
        """
        Initialize a criterion
        :param id: the identifiant of the criterion
        :param texte: the text of the criterion
        :param createur: the creator of the criterion
        :param position: the position of the criterion
        :param colored: if the criterion is colored or in grey
        """
        Scatter.__init__(self)
        self.pos = position
        self.nb_liaisons = 0
        self.identifiant = id
        self.texte = texte
        self.createur = createur
        self.fusionneurs = []
        self.couleur = self.createur.couleur
        self.links = []
        self.size = len(texte) * 1 + 100, 50
        self.colored = colored
        with self.canvas:
            if self.colored:
                Color(self.couleur[0], self.couleur[1], self.couleur[2])
            else:
                Color(.25, .25, .25)
            Ellipse(size=self.size)
            Label(text=self.texte, halign='left', size=self.size)

    def add_link(self, id_img, id_usr):
        """
        Add a link between the criterion and an animal
        :param id_img: the identifiant of the animal
        :param id_usr: the identifiant of the user focussing the animal
        """
        est_dedans = False
        for lien in self.links:
            if lien.linked_to_animal(id_img):
                est_dedans = True
                if lien.linked_to_user(id_usr):
                    self.links.remove(lien)
        if not est_dedans:
            self.links.append(Link(id_img, id_usr))

    def fuse_concept(self, concept):
        """
        Fuse two criterions together
        :param concept: the other criterion ton fuse
        """
        if self.createur.identifiant != concept.createur.identifiant:
            if not self.fusionneurs.__contains__(concept.createur):
                self.fusionneurs.append(concept.createur)

        for fusionneur in concept.fusionneurs:
            if self.createur.identifiant != fusionneur.identifiant:
                if not self.fusionneurs.__contains__(fusionneur):
                    self.fusionneurs.append(fusionneur)

        cpt = 0
        for fusionneur in self.fusionneurs:
            with self.canvas:
                if self.colored:
                    Color(fusionneur.couleur[0], fusionneur.couleur[1], fusionneur.couleur[2])
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
                else:
                    Color(.25, .25, .25)
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
        with self.canvas:
            if self.colored:
                    Color(self.createur.couleur[0], self.createur.couleur[1], self.createur.couleur[2])
                    Ellipse(size=self.size, angle_start=cpt ,angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
            else:
                    Color(.25, .25, .25)
                    Ellipse(size=self.size, angle_start=cpt, angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)

            Label(text=self.texte, halign='left', size=self.size)

        for lien in concept.links:
            self.add_link(lien.id_img, lien.id_usr)
        for fils in self.parent.children:
            if fils.__class__ == Critere and fils.collide_widget(self) and fils != self:
                self.parent.remove_widget(fils)

    def has_link(self, identifiant):
        """
        Return if the criterion is linked to a specified animal
        :param identifiant: The identifiant of the animal
        :return: the position of the animal in the link's table or -1 if the criterion is not linked to the animal
        """
        for lien in self.links :
            if lien.linked_to_animal(identifiant):
                return self.links.index(lien)
        return -1

    def update_link(self, index, center):
        """
        Update the distance and angle between an animal and the criterion
        :param index: the index of hte animal
        :param center: the center of the animal
        """
        self.links[index].update(center, self.center)


    def update(self, dt):
        """
        Update the criterion
        """
        from Animal import Animal
        cpt = 0
        for child in self.parent.children:
            if child.__class__ == Animal :
                if child.collide_point(self.center[0],
                                       self.center[1]) and child.current_utilisateur != None:
                    self.add_link(child.identifiant, child.current_utilisateur.identifiant)
                    child.current_utilisateur.add_link(self.createur.identifiant)
                    child.remove_utilisateur()

        for utilisateur in self.parent.groupe.utilisateurs:
            if utilisateur.validate:
                cpt += 1
        if cpt == 4:
            for child in self.parent.children:
                if child.__class__ == Critere and child.collide_point(self.center[0], self.center[1]) and child != self:
                    self.fuse_concept(child)

    def on_touch_move(self, touch):
        from Animal import Animal
        for child in self.parent.children:
            if child.__class__ == Animal :
                for lien in self.links:
                    if lien.linked_to_animal(child.identifiant):
                        x = self.center_x + lien.distance*math.cos(lien.angle+math.pi)
                        y = self.center_y + lien.distance*math.sin(-lien.angle+math.pi)
                        child.update_coordinate(x,y)
        Scatter.on_touch_move(self,touch)