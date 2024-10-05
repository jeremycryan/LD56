from ant import Ant
from text_previewer import TextPreviewer
from keyboard import Keyboard

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

    def draw(self, surface, offset=(0, 0)):
        surface.fill((0, 0, 0))
        self.text_previewer.draw(surface, offset)
        self.keyboard.draw(surface, offset)
        for ant in self.ants:
            ant.draw(surface, offset)
        for target in self.targets:
            target.draw(surface, offset)

    def on_word_submission(self):
        self.lock_player_input(True)
        self.do_damage()
        self.reset_word()
        self.ant_turn()
        self.lock_player_input(False)

    def lock_player_input(self, locked):
        self.text_previewer.active = not locked

    def do_damage(self):
        self.keyboard.process_word(self.text_previewer.current_string)

    def reset_word(self):
        self.text_previewer.reset_word()

    def ant_turn(self):
        for ant in self.ants:
            ant.advance()
        self.ants += [
            Ant(self.keyboard, self.keyboard.random_horizontal_path()),
            Ant(self.keyboard, self.keyboard.random_horizontal_path()),
            Ant(self.keyboard, self.keyboard.random_vertical_path()),
            Ant(self.keyboard, self.keyboard.random_vertical_path()),
        ]


