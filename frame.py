import pygame

from ant import Ant, Defendant, Mutant
from assets.upgrade_shop import UpgradeShop
from image_manager import ImageManager
from text_previewer import TextPreviewer
from keyboard import Keyboard
import constants as c
from wave import Wave_1, Wave_2, Wave_3, Wave_4


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


class LevelReviewFrame(Frame):
    def __init__(self, game):
        super().__init__(game)
        self.background = ImageManager.load("assets/images/alternate_background.png")
        self.font = pygame.font.Font("assets/fonts/arial.ttf", 14)
        text = c.LETTERS[game.level - 1] + " ".join(self.game.total_words).lower()
        self.text_surf = self.font.render(text, False, (128, 128, 128), wraplength=267)
        self.score = game.score
        self.score_font = pygame.font.Font("assets/fonts/great_answer.ttf", 30)
        self.score_surf = self.score_font.render(f"{self.score}", True, (0, 0, 0))
        self.score_surf.set_alpha(200)
        self.score_surf = pygame.transform.rotate(self.score_surf, 20)

        self.level_clear = ImageManager.load("assets/images/level_clear.png")
        self.time = 0
        self.activated = False

        self.black = pygame.Surface((c.WINDOW_SIZE))
        self.black.fill((0, 0, 0))

        self.since_continue = 0
        self.continued = False

    def update(self, dt, events):
        self.time += dt
        if (self.time > 3 and not self.activated):
            self.activated = True
            self.game.shake(3)
        if self.continued:
            self.since_continue += dt

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.activated:
                        self.continued = True
                        self.game.shake(3)

    def draw(self, surface, offset=(0, 0)):
        surface.blit(self.background, (-50 + offset[0], -66 + offset[1]))
        surface.blit(self.text_surf, (193 + offset[0], 137 + offset[1]))
        surface.blit(self.score_surf, (offset[0] + 65 - self.score_surf.get_width()//2, offset[1] + 60 - self.score_surf.get_height()//2))
        if self.activated:
            surface.blit(self.level_clear, (-50 + offset[0], -66 + offset[1]))

        self.black.set_alpha(255 - 500 * self.time)
        if self.continued:
            self.black.set_alpha(500 * self.since_continue)
            if self.black.get_alpha() >= 255:
                self.done = True
        surface.blit(self.black, (0, 0))


    def next_frame(self):
        return LevelFrame(self.game)


class LevelFrame(Frame):

    def __init__(self, game):
        super().__init__(game)
        self.keyboard = Keyboard(self)
        self.text_previewer = TextPreviewer((320, 50), self.keyboard)
        self.ants = [
        ]
        self.targets = []

        self.state = c.PLAYER_TURN
        self.damage_word = ""
        self.since_damage_instance = 0
        self.particles = []
        self.score = game.score
        self.score_font = pygame.font.Font("assets/fonts/great_answer.ttf", 30)
        self.score_surf = self.score_font.render(f"{self.score}", True, (0, 0, 0))
        self.score_surf.set_alpha(200)
        self.score_surf = pygame.transform.rotate(self.score_surf, 20)
        self.background = ImageManager.load("assets/images/background.png")

        self.upgrades = []
        self.available_upgrades = c.UPGRADES.copy()


        if game.level == 1:
            self.waves = [
                Wave_1,
                Wave_2,
                Wave_3,
                Wave_4,
            ]
        if game.level == 2:
            self.waves = [
                Wave_1,
                Wave_2,
                Wave_3,
                Wave_4,
            ]
        self.active_wave = self.waves.pop(0)(self.keyboard)

        self.ant_turn()

        self.black = pygame.Surface(c.WINDOW_SIZE)
        self.black.fill((0, 0, 0))
        self.should_show_upgrade_screen = False
        self.upgrade_screen_showingness = 0
        self.upgrade_shop = UpgradeShop(self)

        self.level_end_black = self.black.copy()
        self.level_end_black_alpha = 255
        self.level_ending = False

        self.sticky_surf = None

        self.total_words = []

    def player_has_upgrade(self, key):
        for upgrade in self.upgrades:
            if upgrade[0].lower() == key.lower():
                return True
        return False

    def upgrades_player_could_pick(self):
        valid = []
        for upgrade in self.available_upgrades:
            if upgrade[0] not in c.DEPENDENCIES:
                valid.append(upgrade)
                continue
            has_all_dependencies = True
            for dependency in c.DEPENDENCIES[upgrade[0]]:
                if not self.player_has_upgrade(dependency):
                    has_all_dependencies = False
                    break
            if has_all_dependencies:
                valid.append(upgrade)
        return valid

    def gain_upgrade(self, key):
        print(f"GAINING UPGRADE WITH KEY: {key}")
        for item in self.available_upgrades[:]:
            if item[0].lower() == key.lower():
                self.available_upgrades.remove(item)
                self.upgrades.append(item)

                if item[0].lower() == "vocab":
                    self.text_previewer.max_word_length = 7
                    self.text_previewer.on_max_string_change()
                elif item[0].lower() == "vocab 2":
                    self.text_previewer.max_word_length = 10
                    self.text_previewer.on_max_string_change()
                elif item[0].lower() == "k-bomb":
                    self.keyboard.letter_to_key["K"].explosive = True
                elif item[0].lower() == "f-bomb":
                    self.keyboard.letter_to_key["F"].explosive = True
                elif item[0].lower() == "h-bomb":
                    self.keyboard.letter_to_key["H"].explosive = True
                elif item[0].lower() == "s_bomb":
                    self.keyboard.letter_to_key["S"].explosive = True

                return


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

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSLASH:
                    self.show_upgrade_screen()

        if self.should_show_upgrade_screen:
            self.upgrade_screen_showingness += 2*dt
            if self.upgrade_screen_showingness > 1:
                self.upgrade_screen_showingness = 1
        else:
            self.upgrade_screen_showingness -= 2*dt
            if self.upgrade_screen_showingness < 0:
                self.upgrade_screen_showingness = 0

        self.upgrade_shop.update(dt, events)

        surviving_ants = [ant for ant in self.ants if not ant.dead and not ant.reached_destination]
        if not surviving_ants and (not self.active_wave or not self.active_wave.ants) and not self.level_ending and not self.should_show_upgrade_screen:
            self.ants = []
            self.show_upgrade_screen()
            # TODO show upgrade screen

        if self.level_ending:
            self.level_end_black_alpha += 800*dt
            if self.level_end_black_alpha > 255:
                self.done = True
        else:
            self.level_end_black_alpha -= 800*dt
            if self.level_end_black_alpha < 0:
                self.level_end_black_alpha = 0



    def show_upgrade_screen(self):
        self.should_show_upgrade_screen = True
        self.upgrade_shop.populate()
        self.lock_player_input(True)
        self.active_wave = None

    def hide_upgrade_screen(self):
        self.should_show_upgrade_screen = False
        self.advance_wave()
        if self.active_wave:
            self.sticky_surf = self.active_wave.help_surf
        else:
            self.sticky_surf = None

    def advance_wave(self):
        print("NEXT WAVE!")
        if not self.waves:
            print("WAVES ALL DONE!")
            self.level_ending = True
            return # TODO advance level
        self.active_wave = self.waves.pop(0)(self.keyboard)
        self.ant_turn()



    def draw(self, surface, offset=(0, 0)):
        surface.blit(self.background, (offset[0] - 50, offset[1] - 66))
        self.text_previewer.draw(surface, offset)
        self.keyboard.draw(surface, offset)
        for particle in self.particles:
            if particle.layer == 1:
                particle.draw(surface, offset)
        for ant in self.ants:
            ant.draw(surface, offset)
        for target in self.targets:
            target.draw(surface, offset)
        self.keyboard.draw_late(surface, offset)
        for particle in self.particles:
            if particle.layer == 2:
                particle.draw(surface, offset)

        surface.blit(self.score_surf, (offset[0] + 65 - self.score_surf.get_width()//2, offset[1] + 60 - self.score_surf.get_height()//2))

        if self.sticky_surf:
            surface.blit(self.sticky_surf, (offset[0] + 485, offset[1] + 182))

        self.black.set_alpha(180 * self.upgrade_screen_showingness)
        surface.blit(self.black, (0, 0))
        self.upgrade_shop.draw(surface, offset)
        self.level_end_black.set_alpha(self.level_end_black_alpha)
        surface.blit(self.level_end_black, (0, 0))

    def on_word_submission(self):
        self.state = c.DAMAGE
        self.lock_player_input(True)
        self.do_damage()
        self.total_words += [self.text_previewer.current_string]



    def lock_player_input(self, locked):
        self.text_previewer.active = not locked

    def do_damage(self):
        self.damage_word = self.text_previewer.current_string
        self.since_damage_instance = 0

    def reset_word(self):
        self.text_previewer.reset_word()

    def ant_turn(self):
        self.reset_word()
        if self.active_wave and self.active_wave.ants:
            wave_ants = self.active_wave.ants.pop(0)
            while not wave_ants and all([ant.dead or ant.reached_destination for ant in self.ants]) and self.active_wave.ants:
                wave_ants = self.active_wave.ants.pop(0)
            self.ants += wave_ants
        for ant in self.ants:
            ant.advance()
        self.lock_player_input(False)
        self.state = c.PLAYER_TURN

    def gain_score(self, amt):
        # TODO add modifiers to score
        amt *= self.text_previewer.calculate_time_multiplier()
        amt = int(round(amt/10, 0) * 10)
        self.score += amt
        self.score_surf = self.score_font.render(f"{self.score}", True, (0, 0, 0))
        self.score_surf.set_alpha(200)
        self.score_surf = pygame.transform.rotate(self.score_surf, 20)
        return amt

    def lose_score(self, amt):
        self.score -= amt
        self.score_surf = self.score_font.render(f"{self.score}", True, (0, 0, 0))
        self.score_surf.set_alpha(200)
        self.score_surf = pygame.transform.rotate(self.score_surf, 20)
        return amt

    def next_frame(self):
        self.game.level += 1
        self.game.total_words = self.total_words
        return LevelReviewFrame(self.game)

