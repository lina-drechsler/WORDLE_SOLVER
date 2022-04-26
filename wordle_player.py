from random import randint


class Wordle:
    def __init__(self, length):
        self.length = length
        self.secret_word = self.get_word()

    def __repr__(self):
        return f"The word is: {self.secret_word}"

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
        target_rep = [ch for ch in self.secret_word]
        target_ch_count = {}
        for ch in target_rep:
            if ch not in target_ch_count:
                target_ch_count[ch] = 0
            target_ch_count[ch] += 1

        guess_rep = [ch for ch in guess]

        # Assign all 2's (correct letter/correct position)
        final_rep = []
        for i, target_ch in enumerate(target_rep):
            guess_ch = guess_rep[i]

            if target_ch == guess_ch:
                final_rep.append(2)
                target_ch_count[guess_ch] -= 1
            else:
                final_rep.append(0)

        # Assign all 1's (correct letter/wrong position)
        for i, target_ch in enumerate(target_rep):
            guess_ch = guess_rep[i]
            if final_rep[i] == 2:
                continue
            else:
                if guess_ch in target_rep and target_ch_count[guess_ch] > 0:
                    final_rep[i] = 1

        return final_rep


game1 = Wordle(5)
print(game1.make_guess("steam"))
print(game1)
