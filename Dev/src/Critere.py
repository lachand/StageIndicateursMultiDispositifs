from kivy.graphics import Ellipse
from kivy.uix.colorpicker import Color
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter


class Critere(Scatter):
    def __init__(self, id, texte, createur, position, colored):
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
        est_dedans = False
        for lien in self.links:
            if id_img == lien[0]:
                est_dedans = True
                if id_usr == lien[1]:
                    self.links.remove([id_img, id_usr])
        if not est_dedans:
            self.links.append([id_img, id_usr])

    def fuse_concept(self, concept):
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
            self.add_link(lien[0], lien[1])
        for fils in self.parent.children:
            if fils.__class__ == Critere and fils.collide_widget(self) and fils != self:
                self.parent.remove_widget(fils)

    def update(self, dt):
        from Animal import Animal
        cpt = 0
        for child in self.parent.children:
            if child.__class__ == Animal and child.collide_point(self.center[0],
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
