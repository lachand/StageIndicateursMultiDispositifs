from kivy.uix.scatter import Scatter
from kivy.lang import Builder
from kivy.uix.colorpicker import Color
from kivy.graphics import Ellipse
from kivy.uix.label import Label

class Critere(Scatter):

    def __init__(self, id, texte, createur, position):
        Scatter.__init__(self)
        self.pos = position
        self.Nb_Liaisons = 0
        self.ID = id
        self.Texte = texte
        self.Createur = createur
        self.couleur = self.Createur.getCouleur()
        self.Links = []
        self.size = len(texte)*10,50
        with self.canvas:
            Color(self.couleur[0],self.couleur[1],self.couleur[2])
            Ellipse(size=(self.size))
            Label(text=self.Texte,halign='left',size=self.size)

    def addLink(self, id_img, id_usr):
        estDedans = False
        for lien in self.Links :
            if id_img == lien[0]:
                estDedans = True
                if id_usr == lien[1]:
                    self.Links.remove([id_img,id_usr])
        if estDedans == False :
            self.Links.append([id_img, id_usr])

    def fuseConcept(self,concept):
        for lien in concept.Links:
            self.addLink(lien[0],lien[1])
        for fils in self.parent.children:
            if fils.__class__ == Critere and fils.collide_widget(self) and fils != self:
                self.parent.remove_widget(fils)


    def update(self, dt):
        from Animal import Animal
        from Utilisateur import Utilisateur
        cpt = 0
        for child in self.parent.children :
            if child.__class__ == Animal and child.collide_point(self.center[0],self.center[1]) and child.getUtilisateur() != None:
                self.addLink(child.getID(), child.getUtilisateur().getID())
                child.removeUtilisateur()

        for utilisateur in self.parent.Utilisateur:
            if utilisateur.getValidate() == True:
                cpt += 1
        if cpt == 4 :
            for child in self.parent.children :
                if child.__class__ == Critere and child.collide_point(self.center[0],self.center[1]) and child != self:
                    self.fuseConcept(child)