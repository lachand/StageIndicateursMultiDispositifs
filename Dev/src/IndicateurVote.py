#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

from kivy.garden.gauge import Gauge
from kivy.graphics import Ellipse
from kivy.uix.colorpicker import Color
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget


class IndicateurVote(Widget):
    """
    A class representing an indicator representing user's votes
    """

    def __init__(self, integrated):
        """
        Initialize the visualisation
        """
        Widget.__init__(self)
        self.integrated = integrated
        self.jauges = []
        if not self.integrated:

            self.label = Label(text='Votes :', size=(50, 15))
            self.label2 = Label(text='Votes :', size=(50, 15))
            self.label3 = Label(text='Votes :', size=(50, 15))
            self.label4 = Label(text='Votes :', size=(50, 15))

    def initialisation(self):
        """
        Initialize the visualisation
        """

        if not self.integrated :
            scatter = Scatter(size=self.label.size, pos=(120, 0), do_rotation=False, do_scale=False,
                              do_translation=False)

            scatter.add_widget(self.label)
            self.add_widget(scatter)

            scatter2 = Scatter(size=self.label.size,
                               pos=(self.get_root_window().width - 225, self.get_root_window().height - 100), do_rotation=False,
                               do_scale=False,
                               do_translation=False, rotation=180)
            scatter2.add_widget(self.label2)
            self.add_widget(scatter2)

            scatter3 = Scatter(size=self.label.size, pos=(70, self.get_root_window().height - 100), do_rotation=False,
                               do_scale=False,
                               do_translation=False, rotation=180)
            scatter3.add_widget(self.label3)
            self.add_widget(scatter3)

            scatter4 = Scatter(size=self.label.size, pos=(self.get_root_window().width - 170, 0), do_rotation=False,
                               do_scale=False,
                               do_translation=False)
            scatter4.add_widget(self.label4)
            self.add_widget(scatter4)

            for user in self.parent.group.users:
                global position, rotation
                if user.identifier == 1:
                    position = 80, -40
                    rotation = 0
                elif user.identifier == 2:
                    position = 80,self.parent.height -85
                    rotation = 180
                elif user.identifier == 3:
                    position = self.parent.width-210,self.parent.height -85
                    rotation = 180
                elif user.identifier == 4:
                    position = self.parent.width-210,-40
                    rotation = 0

                mygauge = Gauge(value=50, size_gauge=50, size_text=0, angle=rotation)
                mygauge.value = 50
                mygauge.pos = position
                self.jauges.append([mygauge, user])
                self.add_widget(mygauge)

        else :
            for user in self.parent.group.users:
                if user.identifier == 1:
                    rotation_start = -90
                    rotation_stop = 0
                    rotation_stop2 = 90
                elif user.identifier == 2:
                    rotation_start = 90
                    rotation_stop = 180
                    rotation_stop2 = 270
                elif user.identifier == 3:
                    rotation_start = -90
                    rotation_stop = 180
                    rotation_stop2 = 270
                elif user.identifier == 4:
                    rotation_start = 270
                    rotation_stop = 0
                    rotation_stop2 = 90
                position = (user.position[0]-175,user.position[1]-175)

                with self.canvas:
                    Color(user.color[0],user.color[1],user.color[2],.75)
                    Ellipse(size =(350, 350), pos = position, angle_start= rotation_start, angle_end = rotation_stop)
                    Color(user.color[0], user.color[1], user.color[2], .5)
                    Ellipse(size=(350, 350), pos = position, angle_start=rotation_stop, angle_end= rotation_stop2)



    def update(self):
        """
        Update the visualization when an user votes
        :param dt:
        """
        if not self.integrated :
            for jauge in self.jauges:
                if len(jauge[1].votes) > 0:
                    votes_oui = jauge[1].votes.count(1)
                    jauge[0].value = (float(votes_oui) / float(len(jauge[1].votes))) * 100.

        else:
            self.canvas.clear()
            for user in self.parent.group.users:
                print "user : " + str(user.identifier)
                if user.identifier == 1:
                    rotation_start = 270
                    rotation_stop = 0
                    rotation_stop2 = 90
                elif user.identifier == 2:
                    rotation_start = 90
                    rotation_stop = 180
                    rotation_stop2 = 270
                elif user.identifier == 3:
                    rotation_start = 90
                    rotation_stop = 180
                    rotation_stop2 = 270
                elif user.identifier == 4:
                    rotation_start = 270
                    rotation_stop = 0
                    rotation_stop2 = 90

                if len(user.votes) > 0 :
                    ratio = user.votes.count(1) / len(user.votes)
                else :
                    ratio = 0.5
                if ratio == 0:
                    ratio = 0.000000001

                size = 200 + 300 * ratio, 200 + 300 * ratio
                size2 = 200 + 300 * (1-ratio), 200 + 300 * (1-ratio)
                position1 = (user.position[0] - size[0]/2,user.position[1] - size[1]/2)
                position2 = (user.position[0] - size2[0]/2,user.position[1] - size2[1]/2)

                with self.canvas:
                    Color(user.color[0], user.color[1], user.color[2], .75)
                    Ellipse(size=size, pos=position1, angle_start=rotation_start, angle_end=rotation_stop)
                    Color(user.color[0], user.color[1], user.color[2], .5)
                    Ellipse(size=size2, pos=position2, angle_start=rotation_stop, angle_end=rotation_stop2)

