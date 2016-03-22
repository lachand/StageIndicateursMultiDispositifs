import pymunk
import random

from kivy.uix.widget import Widget
from kivy.uix.colorpicker import Color
from kivy.graphics import Ellipse

class PhysicalIndicator(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.space = pymunk.Space()
        self.space.gravity = (0,0)
        self.balls = [[],[],[],[]]
        self.ticks_to_next_ball = 10


    def add_ball(self,space, position):
        mass = 1
        radius = 30
        inertia = pymunk.moment_for_circle(mass, 0, radius) # 1
        body = pymunk.Body(mass, inertia) # 2
        x = position[0]
        y = position[1]
        body.position = x, y # 3
        shape = pymunk.Circle(body, radius) # 4
        space.add(body, shape)
        return shape

    def draw_balls(self):
        for balls in self.balls:
            for ball in balls:
                p = int(ball.body.position.x)-ball.radius, int(ball.body.position.y)-ball.radius
                with self.canvas:
                    Color(self.parent.get_user(self.balls.index(balls)+1).color[0], self.parent.get_user(self.balls.index(balls)+1).color[1], self.parent.get_user(self.balls.index(balls)+1).color[2])
                    Ellipse(pos=p,size=[1.5*ball.radius]*2)

    def update(self, dt):
        self.canvas.clear()
        self.ticks_to_next_ball -= 1

        for user in self.parent.group.users:
            if user.nb_criterion > 0 and self.ticks_to_next_ball % (60/user.nb_criterion) <= 0:
                ball_shape = self.add_ball(self.space, user.position)
                self.balls[user.identifier-1].append(ball_shape)

        if self.ticks_to_next_ball == 0:
                self.ticks_to_next_ball = 60

        balls_to_remove = []

        for balls in self.balls:
            for ball in balls:
                xtmp = self.parent.size[0]/2-ball.body.position.x
                ytmp = self.parent.size[1]/2-ball.body.position.y
                ball.body.velocity = xtmp*2, ytmp*2
                ball.unsafe_set_radius(ball.radius - .05)
                if ball.radius <= 0.1:
                    balls_to_remove.append(ball)

        for ball in balls_to_remove:
            for balls in self.balls:
                if balls.count(ball) > 0:
                    self.space.remove(ball, ball.body)
                    balls.remove(ball)

        self.draw_balls()

        self.space.step(dt)