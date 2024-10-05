from ant import Ant
from text_previewer import TextPreviewer
from keyboard import Keyboard
import constants as c

class Frame:
    def __init__(self, game):
        self.game = game
        self.done = False

    def load(self):
        pass

    def update(self, dt, events):
        pass

    def draw(self, surface, offset=(0, 0)):
        surface.fill((128, 128, 128))

    def next_frame(self):
        return Frame(self.game)


class LevelFrame(Frame):

    def __init__(self, game):
        super().__init__(game)
        self.keyboard = Keyboard(self)
        self.text_previewer = TextPreviewer((400, 50), self.keyboard)
        self.ants = [
            Ant(self.keyboard, self.keyboard.random_horizontal_path()),
            Ant(self.keyboard, self.keyboard.random_horizontal_path()),
        ]
        self.targets = []

        self.state = c.PLAYER_TURN
        self.damage_word = ""
        self.since_damage_instance = 0
        self.particles = []

    def update(self, dt, events):
        super().update(dt, events)
        self.text_previewer.update(dt, events)
        self.keyboard.update(dt, events)
        for ant in self.ants[:]:
            ant.update(dt, events)
        for target in self.targets[:]:
            target.update(dt, events)
            if target.destroyed:
                self.targets.remove(target)
        for particle in self.particles[:]:
            particle.update(dt, events)
            if particle.destroyed:
                self.particles.remove(particle)

        if self.state == c.DAMAGE:
            self.since_damage_instance += dt
            if self.since_damage_instance > 0.2 and self.damage_word:
                self.keyboard.process_word(self.damage_word[0])
                self.damage_word = self.damage_word[1:]
                self.since_damage_instance = 0
            if not self.damage_word and self.since_damage_instance > 0.5:
                self.ant_turn()


    def draw(self, surface, offset=(0, 0)):
        surface.fill((0, 0, 0))
        self.text_previewer.draw(surface, offset)
        self.keyboard.draw(surface, offset)
        for particle in self.particles:
            particle.draw(surface, offset)
        for ant in self.ants:
            ant.draw(surface, offset)
        for target in self.targets:
            target.draw(surface, offset)
        self.keyboard.draw_late(surface, offset)

    def on_word_submission(self):
        self.state = c.DAMAGE
        self.lock_player_input(True)
        self.do_damage()


    def lock_player_input(self, locked):
        self.text_previewer.active = not locked

    def do_damage(self):
        self.damage_word = self.text_previewer.current_string
        self.since_damage_instance = 0

    def reset_word(self):
        self.text_previewer.reset_word()

    def ant_turn(self):
        self.reset_word()
        for ant in self.ants:
            ant.advance()
        self.ants += [
            Ant(self.keyboard, self.keyboard.random_horizontal_path()),
            Ant(self.keyboard, self.keyboard.random_horizontal_path()),
            Ant(self.keyboard, self.keyboard.random_vertical_path()),
            Ant(self.keyboard, self.keyboard.random_vertical_path()),
        ]
        self.lock_player_input(False)
        self.state = c.PLAYER_TURN


