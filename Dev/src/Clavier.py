from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from Utilisateur import Utilisateur
from Critere import Critere


class Clavier(Scatter):
    """
    A class representing a keyboard for criterion creation
    """
    def __init__(self, user, color, position, angle):
        """
        Initialize the keyboard
        :param user: the user wich is creating the criterion
        :param color: the color of the user
        :param position: the position of the keyboard
        :param angle: the angle of the keyboard
        """
        Scatter.__init__(self)
        self.user = user
        self.identifier = self.user.identifier
        self.color = color
        self.pos = position
        self.rotation = angle
        ti = TextInput(size_hint=(None, None), backgroud_color=self.color, multiline=False, size=(100, 30))
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
            criterion = Critere(0, value.text, self.user, self.pos, self.parent.colored_criterions)
            self.user.add_criterion_lvl(self.parent.current_lvl)
            self.parent.add_criterion(criterion)
        self.parent.remove_widget(self)
