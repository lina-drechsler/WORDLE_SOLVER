from random import randint
import json


class Wordle:
    def __init__(self, length=5, is_random_word=True, manual_index=0):
        self.length = length
        self.is_random_word = is_random_word
        self.manual_index = manual_index
        if is_random_word:
            self.secret_word = self.set_word()
        else:
            self.secret_word = self.set_word(manual_index)

        self.run_status = True
        self.number_attempts = 0
        self.incorrect_letters = []
        self.incorrect_positions = {x: set() for x in range(self.length)}
        self.guesses_dict = {}

        with open("words.json") as json_data:
            data = json.load(json_data)

            self.possible_words = data[str(self.length)]

    def __repr__(self):
        return f"The word is: {self.secret_word}"

    def set_word(self, manual_index=0):
        """
        Returns a random word of size self.length to be used as the secret word.
        """

        if self.is_random_word == False:
            with open("words.json") as json_data:
                data = json.load(json_data)
            return data[str(self.length)][manual_index]

        file = f"./data/{self.length}.txt"

        words = []
        with open(file, "r") as f:
            for word in f.readlines():
                words.append(word.rstrip())

        index = randint(0, len(words) - 1)
        random_word = words[index]

        return random_word

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

    def make_template(self):
        # Update possible_words based on information from previous guesses
        all_letters = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]

        # template = {}
        # for i in range(self.length):
        #     template[i] = all_letters

        template = {}
        for i in range(self.length):
            template[i] = []

        # First, find all the correct letters/correct positions for the template
        for word, rep in self.guesses_dict.items():
            for i, ch in enumerate(word):
                if rep[i] == 2:
                    template[i] = [ch]

        # Second, find all the correct letters/incorrect positions for the template
        for word, rep in self.guesses_dict.items():
            for i, ch in enumerate(word):
                if rep[i] == 1:
                    self.incorrect_positions[i].add(ch)
                    for j, values in template.items():
                        if ch in values:
                            ch_index = template[j].index(ch)
                            template[j].pop(ch_index)

                        if (
                            j != i
                            and rep[j] != 2
                            and ch not in self.incorrect_positions[j]
                        ):
                            template[j].append(ch)

                    # cur_letters = template[i]
                    # # template[]
                    # # ch_index = template[i].index(ch)
                    # new_letters = []
                    # for letter in all_letters:
                    #     if letter != ch and letter in cur_letters:
                    #         new_letters.append(ch)
                    # template[i] = new_letters

                    # template[i].pop(ch_index)
        # THIS IS WHERE THE INFINITE PROBLEM IS ENDING

        # Add all the incorrect letters to the incorrect_letters list
        for word, rep in self.guesses_dict.items():
            for i, ch in enumerate(word):
                if rep[i] == 0:
                    self.incorrect_letters.append(ch)
                    # cur_letters = template[i]
                    # self.incorrect_letters.append(ch)
            # Last, remove all the incorrect letters from the template

        # for key in template:
        #     tem_letters = template[key]
        #     for i, ch in enumerate(tem_letters):
        #         if ch in self.incorrect_letters:
        #             template[key].pop(i)
        return template

    def find_guess(self):
        """
        Returns the "optimal" first guess based on the character frequency per position
        """
        with open("counts.json") as json_data:
            data = json.load(json_data)
            letter_count_dict = data[str(self.length)]

        # Set the Baseline Guess
        best_guess = self.possible_words[0]
        best_guess_sum = 0

        for i, ch in enumerate(best_guess):
            letter_freq = letter_count_dict[ch][i]
            best_guess_sum += letter_freq

        template = self.make_template()

        possible_guesses = []
        # Loop through all words to find possible words
        for word in self.possible_words[1:]:
            cur_word_sum = 0
            for i, ch in enumerate(word):
                if ch in self.incorrect_letters:
                    continue
                elif len(template[i]) > 0 and ch not in template[i]:
                    continue
                elif ch in self.incorrect_positions[i]:
                    continue
                letter_freq = letter_count_dict[ch][i]
                cur_word_sum += letter_freq

            if cur_word_sum > best_guess_sum:
                best_guess = word
                best_guess_sum = cur_word_sum
        return best_guess

    def make_guess(self, guess):
        self.guesses_dict[guess] = self.result_rep(guess)
        self.number_attempts += 1
        self.possible_words.remove(guess)

        if guess == self.secret_word:
            self.run_status = False

    def solve(self):
        while self.run_status == True:
            cur_guess = self.find_guess()
            self.make_guess(cur_guess)
        return cur_guess

    def get_attempts(self):
        return self.number_attempts

    def get_secret_word(self):
        return self.secret_word


# game1 = Wordle(length=5, is_random_word=False, manual_index=1)
# print(game1)
# final_guess = game1.solve()
# number_attempts = game1.get_attempts()
# print(f"Solved for {final_guess} in {number_attempts}")
