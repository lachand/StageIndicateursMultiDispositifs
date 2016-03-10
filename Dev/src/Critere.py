from kivy.graphics import Ellipse
from kivy.uix.colorpicker import Color
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter


class Critere(Scatter):
    def __init__(self, id, texte, createur, position, colored):
        Scatter.__init__(self)
        self.pos = position
        self.Nb_Liaisons = 0
        self.ID = id
        self.Texte = texte
        self.Createur = createur
        self.fusionneurs = []
        self.couleur = self.Createur.getcouleur()
        self.Links = []
        self.size = len(texte) * 1 + 100, 50
        self.colored = colored
        with self.canvas:
            if self.colored:
                Color(self.couleur[0], self.couleur[1], self.couleur[2])
            else:
                Color(.25, .25, .25)
            Ellipse(size=self.size)
            Label(text=self.Texte, halign='left', size=self.size)

    def addLink(self, id_img, id_usr):
        estDedans = False
        for lien in self.Links:
            if id_img == lien[0]:
                estDedans = True
                if id_usr == lien[1]:
                    self.Links.remove([id_img, id_usr])
        if not estDedans:
            self.Links.append([id_img, id_usr])

    def fuseConcept(self, concept):
        if self.Createur.getid() != concept.Createur.getid() :
            if not self.fusionneurs.__contains__(concept.Createur) :
                self.fusionneurs.append(concept.Createur)

        for fusionneur in concept.fusionneurs :
            if self.Createur.getid() != fusionneur.getid() :
                if not self.fusionneurs.__contains__(fusionneur) :
                    self.fusionneurs.append(fusionneur)

        cpt = 0
        for fusionneur in self.fusionneurs:
            with self.canvas:
                if self.colored:
                    Color(fusionneur.Couleur[0], fusionneur.Couleur[1], fusionneur.Couleur[2])
                    Ellipse(size=self.size,angle_start=cpt,angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
                else:
                    Color(.25, .25, .25)
                    Ellipse(size=self.size,angle_start=cpt,angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
        with self.canvas:
            if self.colored:
                    Color(self.Createur.Couleur[0], self.Createur.Couleur[1], self.Createur.Couleur[2])
                    Ellipse(size=self.size,angle_start=cpt,angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)
            else:
                    Color(.25, .25, .25)
                    Ellipse(size=self.size,angle_start=cpt,angle_end=cpt+(360/(len(self.fusionneurs)+1)))
                    cpt += 360/(len(self.fusionneurs)+1)

            Label(text=self.Texte, halign='left', size=self.size)

        for lien in concept.Links:
            self.addLink(lien[0], lien[1])
        for fils in self.parent.children:
            if fils.__class__ == Critere and fils.collide_widget(self) and fils != self:
                self.parent.remove_widget(fils)

    def update(self, dt):
        from Animal import Animal
        cpt = 0
        for child in self.parent.children:
            if child.__class__ == Animal and child.collide_point(self.center[0],
                                                                 self.center[1]) and child.getUtilisateur() != None:
                self.addLink(child.getid(), child.getUtilisateur().getid())
                child.getUtilisateur().addLink(self.Createur.getid())
                child.removeUtilisateur()

        for utilisateur in self.parent.getUtilisateurs():
            if utilisateur.getValidate():
                cpt += 1
        if cpt == 4:
            for child in self.parent.children:
                if child.__class__ == Critere and child.collide_point(self.center[0], self.center[1]) and child != self:
                    self.fuseConcept(child)
