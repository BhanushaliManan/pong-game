from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from random import randint
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivymd.toast import toast
from kivy_deps import sdl2, glew

Window.set_icon('Icon.png')
Config.set('kivy', 'window_icon', 'Icon.png')


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.1


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        # Latest Position = Current Velocity + Current Position
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    # For Keyboard
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.player1.center_y += 10
        elif keycode[1] == 's':
            self.player1.center_y -= 10
        elif keycode[1] == 'up':
            self.player2.center_y += 10
        elif keycode[1] == 'down':
            self.player2.center_y -= 10
        return True

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

        # For Keyboard
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):

        self.ball.move()

        # Bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # Bounce off left
        if self.ball.x < 0:
            # Ball Touched Player 1 Side, Score To Player 2
            self.ball.velocity_x *= -1
            self.player2.score += 1
            toast("Score To Player 2")
            self.serve_ball()

        # bounce off right
        if self.ball.right > self.width:
            # Ball Touched Player 2 Side, Score To Player 1
            self.ball.velocity_x *= -1
            self.player1.score += 1
            toast("Score To Player 1")
            self.serve_ball()

        # Bounce Off Paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width / 1 / 4:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3 / 4:
            self.player2.center_y = touch.y


class Manager(ScreenManager):
    pass


class PongGameApp(App):
    title = "Pong Game"
    icon = 'Icon.png'

    def build(self):
        self.load_kv('pong.kv')
        Window.maximize()
        return Manager(transition=FadeTransition())


PongGameApp().run()
