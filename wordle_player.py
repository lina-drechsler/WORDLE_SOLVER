class Wordle:
    def __init__(self, length):
        self.secret_word = self.get_word()
        self.length = length

    def get_word(self):
        """
        Returns a random word of size self.length to be used as the secret word.
        """

        return "WORDLE"

    def make_guess(self, guess):
        """
        Returns the resulting representation of a word guess.

        Correct Letter/Correct Position: 2
        Correct Letter/Wrong Position: 1
        Wrong Letter/Wrong Position: 0
        """

        return [2, 2, 2, 2, 2]
