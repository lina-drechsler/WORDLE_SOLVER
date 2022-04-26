from random import randint


class Wordle:
    def __init__(self, length=5, is_random_word=True):
        self.length = length
        self.secret_word = self.set_word()
        self.is_random_word = is_random_word
        self.run_status = True
        self.number_attempts = 0
        self.guesses_dict = {}

    def __repr__(self):
        return f"The word is: {self.secret_word}"

    def set_word(self, manual_index=0):
        """
        Returns a random word of size self.length to be used as the secret word.
        """
        import json

        if self.is_random_word == False:
            with open("words.json") as json_data:
                data = json.loads(json_data)
            return data[str(self.length)][manual_index]

        file = f"./data/{self.length}.txt"

        words = []
        with open(file, "r") as f:
            for word in f.readlines():
                words.append(word.rstrip())

        index = randint(0, len(words) - 1)
        random_word = words[index]

        return random_word

    # def find_guess(self):
    #     """
    #     Returns the "optimal" guess
    #     """
    #     import json

    #     with open("words.json") as json_data:
    #          data = json.loads(json_data)
    #          possible_words = data[str(self.length)]

    #     with open("XXXXXX.json") as json_data:
    #         data = json.loads(json_data)
    #         letter_count_dict = data[str(self.length)]

    #     for

    def result_rep(self, guess):
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

    def make_guess(self, guess):
        self.guesses_dict[guess] = self.result_rep(guess)
        self.number_attempts += 1

        if guess == self.secret_word:
            self.run_status = False
