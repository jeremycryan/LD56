import time

import pygame

from ant import Ant, Defendant, Mutant
from upgrade_shop import UpgradeShop
from image_manager import ImageManager
from sound_manager import SoundManager
from text_previewer import TextPreviewer
from keyboard import Keyboard
import constants as c
from wave import Wave_1, Wave_2, Wave_3, Wave_4, Wave_5, Wave_6, Wave_7


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

class ScoreFrame(Frame):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.music.set_volume(0.25)

        self.score = game.score
        self.score_font = pygame.font.Font("assets/fonts/great_answer.ttf", 50)
        self.score_surf = self.score_font.render(f"{self.game.score}", False, (255, 255, 255))
        self.time = 0
        self.enter_to_continue = ImageManager.load("assets/images/enter_to_continue.png")
        self.continued = False
        self.since_continue = 0

        self.black = pygame.Surface((c.WINDOW_SIZE))
        self.black.fill((0, 0, 0))

        self.background = ImageManager.load("assets/images/final_score.png")

    def update(self, dt, events):
        self.time += dt
        self.since_continue += dt

        if self.time > 3:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not self.continued:
                            self.continued = True
                            self.since_continue = 0
                            print("BLARG")


    def draw(self, surface, offset=(0, 0)):
        surface.blit(self.background, (-50, -50))
        surface.blit(self.score_surf, (c.WINDOW_WIDTH//2 - self.score_surf.get_width()//2, c.WINDOW_HEIGHT//2 - 50))
        if self.time > 3 and self.time % 1 < 0.7:
            surface.blit(self.enter_to_continue, (c.WINDOW_WIDTH//2 - self.enter_to_continue.get_width()//2, c.WINDOW_HEIGHT - 25))

        self.black.set_alpha(255 - 500 * self.time)
        if self.continued:
            self.black.set_alpha(500 * self.since_continue)
            if self.black.get_alpha() >= 255:
                self.done = True
        surface.blit(self.black, (0, 0))

    def next_frame(self):
        self.game.reset()
        return LevelFrame(self.game)


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

        self.fanfare = SoundManager.load("assets/audio/fanfare.ogg")
        self.fanfare.set_volume(0.3)

        self.upgrade_sfx = SoundManager.load("assets/audio/upgrade.wav")
        self.upgrade_sfx.set_volume(0.2)

        pygame.mixer.music.set_volume(0.05)

    def update(self, dt, events):
        self.time += dt
        if (self.time > 3 and not self.activated):
            self.activated = True
            self.game.shake(3)
            self.fanfare.play()
        if self.continued:
            self.since_continue += dt

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.activated:
                        self.continued = True
                        self.game.shake(3)
                        self.upgrade_sfx.play()


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
        pygame.mixer.music.set_volume(0.5)
        if self.game.level <= 3:
            return LevelFrame(self.game)
        else:
            return ScoreFrame(self.game)


class IntroFrame(Frame):
    def __init__(self, game):
        super().__init__(game)
        self.background = ImageManager.load("assets/images/background.png")
        self.keyboard = Keyboard(self)
        self.outside_keyboard_cover = ImageManager.load("assets/images/outside_keyboard_cover.png")
        self.font = pygame.font.Font("assets/fonts/arial.ttf", 14)
        self.aaaaa = ImageManager.load("assets/images/aaaaa.png")
        self.full_of_ants = ImageManager.load("assets/images/full_of_ants.png")

        self.level_clear = ImageManager.load("assets/images/level_clear.png")
        self.time = 0
        self.activated = False

        self.black = pygame.Surface((c.WINDOW_SIZE))
        self.black.fill((0, 0, 0))

        self.since_continue = 0
        self.continued = False
        self.since_blip = 0

        self.blip = SoundManager.load("assets/audio/talk.wav")
        self.blip.set_volume(0.12)
        self.scream = SoundManager.load("assets/audio/scream.wav")
        self.scream.set_volume(0.3)


        self.ants = [
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), 1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), 1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), 1),
        ]


    def update(self, dt, events):
        self.time += dt
        self.since_blip += dt
        if (self.time > 3 and not self.activated):
            self.activated = True
            # self.game.shake(3)
        if (self.time > 4 and self.time < 6):
            self.game.shake_amp = 3
            if self.since_blip > 0.05:
                self.since_blip = 0
                self.scream.play()
        if (self.time > 8 and self.time < 11):
            self.game.shake_amp = 2
            if self.since_blip > 0.12:
                self.since_blip = 0
                self.blip.play()
        if self.time > 13:
            self.continued = True
        if self.continued:
            self.since_continue += dt

        for ant in self.ants:
            ant.sprite.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        surface.blit(self.background, (-50 + offset[0], -66 + offset[1]))
        self.keyboard.draw(surface, offset)

        positions = [(200 + offset[0], 200 + offset[1]), (350 + offset[0], 220 + offset[1]), (300 + offset[0], 150 + offset[1])]
        for ant in self.ants:
            img = ant.sprite.get_image()
            pos = positions.pop(0)
            surface.blit(img, pos)

        yoff = max(0, (self.time - 3) * 8)**2
        alpha = 255 - max(0, (self.time - 3) * 400)
        self.outside_keyboard_cover.set_alpha(alpha)
        surface.blit(self.outside_keyboard_cover, (offset[0], offset[1] - yoff))

        if (self.time > 4 and self.time < 6):
            surface.blit(self.aaaaa, (offset[0], offset[1]))
        elif (self.time > 8 and self.time < 11):
            surface.blit(self.full_of_ants, offset)
        # if self.activated:
        #     surface.blit(self.level_clear, (-50 + offset[0], -66 + offset[1]))

        self.black.set_alpha(255 - 500 * self.time)
        if self.continued:
            self.black.set_alpha(500 * self.since_continue)
            if self.black.get_alpha() >= 255:
                self.done = True
        surface.blit(self.black, (0, 0))


    def next_frame(self):
        pygame.mixer.music.load("assets/audio/music.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
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
        self.enter_to_continue = ImageManager.load("assets/images/enter_to_continue.png")

        self.upgrades = []
        self.available_upgrades = c.UPGRADES.copy()
        pygame.mixer.music.set_volume(0.5)



        self.tutorial = ImageManager.load("assets/images/tutorial.png")
        if self.game.level == 1:
            self.tutorial_showing = True
            self.tutorial.set_alpha(255)
            self.lock_player_input(True)
        else:
            self.tutorial.set_alpha(0)
            self.tutorial_showing = False

        if game.level == 1:
            self.waves = [
                Wave_1,
                Wave_2,
            ]
        if game.level == 2:
            self.waves = [
                Wave_3,
                Wave_4,
            ]
        if game.level == 3:
            self.waves = [
                Wave_5,
                Wave_6,
                Wave_7,
            ]
        self.active_wave = self.waves.pop(0)(self.keyboard)
        if self.active_wave:
            self.sticky_surf = self.active_wave.help_surf
        else:
            self.sticky_surf = None

        self.ant_turn()

        self.black = pygame.Surface(c.WINDOW_SIZE)
        self.black.fill((0, 0, 0))
        self.should_show_upgrade_screen = False
        self.upgrade_screen_showingness = 0
        self.upgrade_shop = UpgradeShop(self)

        self.level_end_black = self.black.copy()
        self.level_end_black_alpha = 255
        self.level_ending = False

        self.rare_letter_modifier = 2

        self.spree_level = 0
        self.ants_killed_this_turn = 0

        self.total_words = []

        for upgrade in self.game.upgrades:
            if not self.player_has_upgrade(upgrade[0]):
                self.gain_upgrade(upgrade[0])

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
                elif item[0].lower() == "s-bomb":
                    self.keyboard.letter_to_key["S"].explosive = True
                elif item[0].lower() == "sphinx":
                    self.rare_letter_modifier = 4
                elif item[0].lower() == "sphinx 2":
                    self.rare_letter_modifier = 6
                elif item[0].lower() == "speedy":
                    self.text_previewer.max_time_multiplier = 2.5
                elif item[0].lower() == "speedy 2":
                    self.text_previewer.max_time_multiplier = 3.0
                elif item[0].lower() == "spree":
                    self.spree_level = 1
                elif item[0].lower() == "spree 2":
                    self.spree_level = 2
                elif item[0].lower() == "coffee":
                    pygame.display.set_caption(f"{c.CAPTION} - CAFFEINATED")
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

        # for event in events:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_BACKSLASH:
        #             self.show_upgrade_screen()

        if self.should_show_upgrade_screen:
            self.upgrade_screen_showingness += 2*dt
            if self.upgrade_screen_showingness > 1:
                self.upgrade_screen_showingness = 1
        else:
            self.upgrade_screen_showingness -= 2*dt
            if self.upgrade_screen_showingness < 0:
                self.upgrade_screen_showingness = 0

        pygame.mixer.music.set_volume(0.5 - 0.43*self.upgrade_screen_showingness)

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

        self.upgrade_shop.update(dt, events)

        if not self.tutorial_showing:
            self.tutorial.set_alpha(self.tutorial.get_alpha() - 500*dt)
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.tutorial_showing = False
                        self.lock_player_input(False)
                        self.upgrade_shop.upgrade_sfx.play()

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

        if self.tutorial.get_alpha() > 0:
            surface.blit(self.tutorial, (-50, -50))
            if time.time()%1 < 0.7:
                surface.blit(self.enter_to_continue, (c.WINDOW_WIDTH//2 - self.enter_to_continue.get_width()//2, c.WINDOW_HEIGHT - 28))

        surface.blit(self.level_end_black, (0, 0))

    def on_word_submission(self):
        self.ants_killed_this_turn = 0
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
        self.ants_killed_this_turn = 0
        self.reset_word()
        if self.active_wave and self.active_wave.ants:
            wave_ants = self.active_wave.ants.pop(0)
            while not wave_ants and all([ant.dead or ant.reached_destination for ant in self.ants]) and self.active_wave.ants:
                wave_ants = self.active_wave.ants.pop(0)
            self.ants += wave_ants
        for ant in self.ants:
            ant.on_ant_turn()
            ant.advance()
        if not self.tutorial_showing:
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
        self.game.score = self.score
        self.game.upgrades = self.upgrades
        return LevelReviewFrame(self.game)

