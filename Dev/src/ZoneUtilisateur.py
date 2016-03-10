from kivy.uix.widget import Widget

from Clavier import Clavier


class ZoneUtilisateur(Widget):
    def __init__(self, utilisateur, position):
        self.Utilisateur = utilisateur
        self.Taille = [300, 300]
        self.Position = position[0] - self.Taille[0] / 2, position[1] - self.Taille[1] / 2
        self.Couleur = self.Utilisateur.getcouleur()
        Widget.__init__(self)

    def on_touch_down(self, touch):
        global position, rotation
        if touch.is_double_tap and self.collide_point(touch.x, touch.y):
            if self.getID() == 1:
                position = self.get_root_window().width / 2, 200
                rotation = 0
            elif self.getID() == 2:
                position = self.get_root_window().width - 300, self.get_root_window().height / 2
                rotation = 90
            elif self.getID() == 3:
                position = self.get_root_window().width / 2, self.get_root_window().height - 300
                rotation = 180
            elif self.getID() == 4:
                position = 200, self.get_root_window().height / 2
                rotation = -90
            clav = Clavier(self.Utilisateur, self.Couleur, position, rotation)
            self.parent.add_widget(clav)
        if self.collide_point(touch.x, touch.y):
            self.Utilisateur.Validate()

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.Utilisateur.Unvalidate()

    def getID(self):
        return self.Utilisateur.getid()

    def getUtilisateur(self):
        return self.Utilisateur
