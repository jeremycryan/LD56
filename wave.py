from ant import Ant, Defendant, Mutant, Persistant
from image_manager import ImageManager


class Wave:

    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.ants = []
        self.load_ants()
        self.help_surf = self.load_help_surf()

    def load_ants(self):
        pass

    def load_help_surf(self):
        return None

class Wave_1(Wave):
    def load_ants(self):
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
        ])
        self.ants.append([])
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
        ])
        self.ants.append([])
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
        ])

class Wave_2(Wave):
    def load_ants(self):
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed = 4),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4)
        ])
        self.ants.append([])
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4)
        ])
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4)
        ])
        self.ants.append([])
        self.ants.append([
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
        ])

    def load_help_surf(self):
        return ImageManager.load("assets/images/mutant_help.png")

class Wave_4(Wave):
    def load_ants(self):
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
        ])
        self.ants.append([
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
            Mutant(self.keyboard, self.keyboard.random_vertical_path(), speed=2),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
        ])
        self.ants.append([])
        self.ants.append([])
        self.ants.append([])
        self.ants.append([])
        self.ants.append([
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
        ])


class Wave_3(Wave):
    def load_ants(self):
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed = 1),
        ])
        self.ants.append([])
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed = 1),
        ])
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed = 1),
        ])
        self.ants.append([])
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
        ])


    def load_help_surf(self):
        return ImageManager.load("assets/images/defendant_help.png")

class Wave_5(Wave):
    def load_ants(self):
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Persistant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Persistant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
        ])
        self.ants.append([])
        self.ants.append([
            Persistant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Persistant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Persistant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Persistant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Persistant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
        ])
        self.ants.append([])
        self.ants.append([])
        self.ants.append([
            Persistant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Persistant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
        ])
        self.ants.append([
            Persistant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
        ])
        self.ants.append([
            Persistant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Persistant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
        ])

    def load_help_surf(self):
        return ImageManager.load("assets/images/persistant_help.png")


class Wave_6(Wave):
    def load_ants(self):
                self.ants.append([
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                ])
                self.ants.append([
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                ])
                self.ants.append([
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                ])
                self.ants.append([])
                self.ants.append([])
                self.ants.append([
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                ])
                self.ants.append([
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                ])
                self.ants.append([
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                    Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
                ])

class Wave_7(Wave):
    def load_ants(self):
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Mutant(self.keyboard, self.keyboard.random_vertical_path(), speed=2),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
            Mutant(self.keyboard, self.keyboard.random_vertical_path(), speed=2),
            Persistant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
        ])
        self.ants.append([])
        self.ants.append([])
        self.ants.append([])
        self.ants.append([
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Ant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_horizontal_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Defendant(self.keyboard, self.keyboard.random_vertical_path(), speed=1),
            Persistant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Persistant(self.keyboard, self.keyboard.random_horizontal_path(), speed=2),
            Mutant(self.keyboard, self.keyboard.random_vertical_path(), speed=2),
            Mutant(self.keyboard, self.keyboard.random_horizontal_path(), speed=4),
            Mutant(self.keyboard, self.keyboard.random_vertical_path(), speed=2),
        ])
