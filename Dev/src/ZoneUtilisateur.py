from kivy.uix.widget import Widget

from Clavier import Clavier


class ZoneUtilisateur(Widget):
    """
    A class to represent the indicator of the user's zone
    """
    def __init__(self, utilisateur, position):
        """
        Initialize the indicator
        :param utilisateur: the user of wich the indicator is about
        :param position: the position of the indicator
        """
        self.utilisateur = utilisateur
        self.taille = [300, 300]
        self.position = position[0] - self.taille[0] / 2, position[1] - self.taille[1] / 2
        self.couleur = self.utilisateur.couleur
        Widget.__init__(self)

    def on_touch_down(self, touch):
        """
        Define actions to perfom when the indicator is touched down
        :param touch: the touch point (position, type of touch, ...)
        """
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
        """
        Define actions to perfom when the indicator is touched up
        :param touch: the touch point (position, type of touch, ...)
        """
        if self.collide_point(touch.x, touch.y):
            self.utilisateur.validate = False
