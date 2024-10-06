WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

WINDOW_SCALE = 2
SCALED_WINDOW_SIZE = WINDOW_WIDTH*WINDOW_SCALE, WINDOW_HEIGHT*WINDOW_SCALE

FRAMERATE = 100

CAPTION = "LD56"

QWERTY_LAYOUT = "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"

ALL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RARE_LETTERS = "QZXJ"
UNCOMMON_LETTERS = "KVBPGWY"
COMMON_LETTERS = "".join(letter for letter in ALL_LETTERS if letter not in RARE_LETTERS + UNCOMMON_LETTERS)

RIGHT = 0
UP_RIGHT = 1
UP_LEFT = 2
LEFT = 3
DOWN_LEFT = 4
DOWN_RIGHT = 5

PLAYER_TURN = 0
DAMAGE = 1
ANT_TURN = 2

UPGRADES = [
    ("Quartz Sphinx", "Rare letter multiplier is increased to 400%."),
    ("Vocab", "Words can be up to 7 letters."),
    ("Vocab 2", "Words can be up to 10 letters"),
    ("K-Bomb", "The K key explodes when you press it."),
    ("S-Bomb", "The S key explodes when you press it."),
    ("H-Bomb", "No, not that kind. You know the drill."),
    ("F-Bomb", "You saw this one coming."),
    ("Speedy", "Max speed multiplier is increased to 250%."),
    ("Speedy 2", "Max speed multiplier is increased to 300%."),
    ("Double Tap", "Hitting an ant you just killed gives bonus points."),
    ("Double Tap 2", "Double tap bonus increased to 200."),
    ("Coffee", "Drink a delicious cup of coffee."),
    # ("Big Word Bad", "Word with four or less go boom."),
]

DEPENDENCIES = {
    "Vocab 2": ("Vocab",),
    "F-Bomb": ("H-Bomb",),
    "H-Bomb": ("S-Bomb",),
    "S-Bomb": ("K-Bomb",),
    "Speedy 2": ("Speedy",),
    "Double Tap 2": ("Double Tap",),
    "Coffee": ("K-Bomb", "Vocab", "Speedy", "Double Tap"),
}

LETTERS = {
    1: "Dearest employer,\n\nRegarding the sales report due earlier today,\n\n"
}