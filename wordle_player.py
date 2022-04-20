from random import randint


class Wordle:
    def __init__(self, length):
        self.length = length
        self.secret_word = self.get_word()

    def get_word(self):
        """
        Returns a random word of size self.length to be used as the secret word.
        """
        file = f"./data/{self.length}.txt"

        words = []
        with open(file, "r") as f:
            for word in f.readlines():
                words.append(word.rstrip())

        index = randint(0, len(words) - 1)
        random_word = words[index]

        return random_word

    def make_guess(self, guess):
        """
        Returns the resulting representation of a word guess.

        Correct Letter/Correct Position: 2
        Correct Letter/Wrong Position: 1
        Wrong Letter/Wrong Position: 0
        """

        return [2, 2, 2, 2, 2]


word1 = Wordle(5)
print(word1.secret_word)
