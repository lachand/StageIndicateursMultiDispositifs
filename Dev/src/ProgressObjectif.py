from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget


class ProgressObjectif(Widget):
    """
    A class to represent the indicator representing the progress comparing to objectives
    """
    def __init__(self, objective, position, level_max):
        """
        Initialize the indicator
        :param objective: a table of differents objectives
        :param position: the position of the indicator
        :param level_max: the max number of objectives
        """
        Widget.__init__(self)
        self.objective = objective
        self.progress = 0
        self.level = 0
        self.level_max = level_max

        btn_new_image = Button(text='news images', size=[200, 50])
        btn_new_image.pos = (position[0] - btn_new_image.width / 2, position[1])
        btn_new_image.bind(on_press=self.callback)

        self.pb = ProgressBar(max=self.objective, value=self.progress, size=[200, 0])
        self.pb.pos = (position[0] - self.pb.width / 2, position[1] + btn_new_image.height)
        self.add_widget(btn_new_image)
        self.add_widget(self.pb)

    def update(self, dt):
        """
        Update the indicator when criterions are created
        """
        self.progress = len(self.parent.criterions)
        self.pb.value = self.progress

    def callback(instance, value):
        """
        Add new animals to the table if the current objective is done
        """
        if instance.progress >= instance.objective and instance.level < instance.level_max:
            table = instance.parent
            table.current_lvl += 1
            instance.level += 1
            instance.objective = instance.parent.news_images(instance.level)
            instance.pb.max = instance.objective
