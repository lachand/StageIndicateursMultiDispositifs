from kivy.uix.widget import Widget
from kivy.lang import Builder
from Clavier import Clavier
#Builder.load_file('template.kv')


class ZoneUtilisateur(Widget):

    def __init__(self,utilisateur, position):
        self.Utilisateur = utilisateur
        self.Taille = [300,300]
        self.Position = position[0]-self.Taille[0]/2 ,position[1]-self.Taille[1]/2
        self.Couleur = self.Utilisateur.getCouleur()
        Widget.__init__(self)

    def on_touch_down(self, touch):
        if touch.is_double_tap and self.collide_point(touch.x,touch.y):
            if self.getID() == 1:
                position = self.get_root_window().width/2,200
                rotation = 0
            elif self.getID() == 2:
                position = self.get_root_window().width-(300),self.get_root_window().height/2
                rotation = 90
            elif self.getID() == 3:
                position = self.get_root_window().width/2,self.get_root_window().height-(300)
                rotation = 180
            elif self.getID() == 4:
                position = 200,self.get_root_window().height/2
                rotation = -90
            print self.Couleur
            clav = Clavier(self.Utilisateur,self.Couleur,position,rotation)
            self.parent.add_widget(clav)
        self.Utilisateur.Validate()

    def on_touch_up(self, touch):
        self.Utilisateur.Unvalidate()

    def getID(self):
        return self.Utilisateur.getID()

    def getUtilisateur(self):
        return self.Utilisateur