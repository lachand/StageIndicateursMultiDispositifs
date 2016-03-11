from kivy.uix.widget import Widget

from Clavier import Clavier


class ZoneUtilisateur(Widget):
    def __init__(self, utilisateur, position):
        self.utilisateur = utilisateur
        self.taille = [300, 300]
        self.position = position[0] - self.taille[0] / 2, position[1] - self.taille[1] / 2
        self.couleur = self.utilisateur.couleur
        Widget.__init__(self)

    def on_touch_down(self, touch):
        global position, rotation
        if touch.is_double_tap and self.collide_point(touch.x, touch.y):
            if self.utilisateur.identifiant == 1:
                position = self.get_root_window().width / 2, 200
                rotation = 0
            elif self.utilisateur.identifiant == 2:
                position = self.get_root_window().width - 300, self.get_root_window().height / 2
                rotation = 90
            elif self.utilisateur.identifiant == 3:
                position = self.get_root_window().width / 2, self.get_root_window().height - 300
                rotation = 180
            elif self.utilisateur.identifiant == 4:
                position = 200, self.get_root_window().height / 2
                rotation = -90
            clav = Clavier(self.utilisateur, self.couleur, position, rotation)
            self.parent.add_widget(clav)
        if self.collide_point(touch.x, touch.y):
            self.utilisateur.validate = True

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.utilisateur.validate = False
