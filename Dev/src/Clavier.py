from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from Utilisateur import Utilisateur
from Critere import Critere


class Clavier(Scatter):
    """
    A class representing a keyboard for criterion creation
    """
    def __init__(self, utilisateur, couleur, position, angle):
        """
        Initialize the keyboard
        :param utilisateur: the user wich is creating the criterion
        :param couleur: the color of the user
        :param position: the position of the keyboard
        :param angle: the angle of the keyboard
        """
        Scatter.__init__(self)
        self.utilisateur = utilisateur
        self.identifiant = self.utilisateur.identifiant
        self.couleur = couleur
        self.pos = position
        self.rotation = angle
        ti = TextInput(size_hint=(None, None), backgroud_color=self.couleur, multiline=False, size=(100, 30))
        ti.bind(on_text_validate=self.validate)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False
        self.add_widget(ti)

    def validate(self, value):
        """
        Validate the creation of the criterion
        """
        if len(value.text) != 0:
            critere = Critere(0, value.text, self.utilisateur, self.pos, self.parent.colored_criteres)
            self.utilisateur.add_critere_lvl(self.parent.current_lvl)
            self.parent.add_critere(critere)
        self.parent.remove_widget(self)
