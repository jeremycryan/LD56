class WordManager:
    WORDS = set()

    @staticmethod
    def init():
        with open("assets/words_alpha.txt") as f:
            while line := f.readline():
                line = line.strip().upper()
                if len(line) < 1:
                    continue
                if len(line) > 15:
                    continue
                WordManager.WORDS.add(line)

    @staticmethod
    def contains(string):
        return string.upper() in WordManager.WORDS