from kivy.uix.widget import Widget
from Critere import Critere
from Animal import Animal
from kivy.uix.colorpicker import Color
from kivy.graphics import Line


class Links(Widget):
    """
    A class to view all links on the table
    """
    def __init__(self, colored):
        """
        Initialize the canvas containing links
        :param colored: if the links are colored or grey
        """
        self.colored = colored
        Widget.__init__(self)

    def update(self, dt):
        """
        Update the view of links
        """
        self.canvas.clear()
        for child in self.parent.children:
            if child.__class__ == Critere:
                for link in child.links:
                    for child2 in self.parent.children:
                        if child2.__class__ == Animal and link.linked_to_animal(child2.identifier):
                            user = self.parent.get_user(link.id_usr)
                            with self.canvas:
                                if self.colored:
                                    color = user.color
                                    Color(color[0], color[1], color[2])
                                else:
                                    Color(.25, .25, .25)
                                Line(points=[child.center[0], child.center[1], child2.center[0], child2.center[1]],
                                     width=2)
