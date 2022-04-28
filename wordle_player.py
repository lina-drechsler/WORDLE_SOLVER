from random import randint


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
        template = {}
        for i in range(self.length):
            template[i] = all_letters

        incorrect_letters = []

        if len(self.guesses_dict) > 0:
            # First, find all the correct letters/correct positions for the template
            print(list(self.guesses_dict.items())[-1])
            word, rep = list(self.guesses_dict.items())[-1]
            for i, ch in enumerate(word):
                if rep[i] == 2:
                    template[i] = [ch]
            # Second, find all the correct letters/incorrect positions for the template
            # THIS IS WHERE THE INFINITE PROBLEM IS OCCURING
            # word, rep = list(self.guesses_dict.items())[-1]
            for i, ch in enumerate(word):
                # print(i, ch)
                # print(rep[i])
                # print("----------")
                if ch in template[i] and rep[i] == 1:
                    # print(f"'1' rep: {ch}")
                    # print(template[i])
                    ch_index = template[i].index(ch)
                    # print(ch_index)
                    template[i].pop(ch_index)
                    # print(template[i])
            # THIS IS WHERE THE INFINITE PROBLEM IS ENDING

            # Add all the incorrect letters to the incorrect_letters list
            # word, rep = list(self.guesses_dict.items())[-1]
            for i, ch in enumerate(word):
                if rep[i] == 0:
                    incorrect_letters.append(ch)
            # Last, remove all the incorrect letters from the template
            for key in template:
                tem_letters = template[key]
                for i, ch in enumerate(tem_letters):
                    if ch in incorrect_letters:
                        template[key].pop(i)

        return template

    def find_guess(self):
        """
        Returns the "optimal" first guess based on the character frequency per position
        """
        import json

        with open("words.json") as json_data:
            data = json.load(json_data)
            possible_words = data[str(self.length)]

        with open("counts.json") as json_data:
            data = json.load(json_data)
            letter_count_dict = data[str(self.length)]

        # Set the Baseline Guess
        best_guess = possible_words[0]
        best_guess_sum = 0

        for i, ch in enumerate(best_guess):
            letter_freq = letter_count_dict[ch][i]
            best_guess_sum += letter_freq

        template = self.make_template()

        # Loop through all words to find best guess
        for word in possible_words[1:]:
            cur_word_sum = 0
            for i, ch in enumerate(word):
                if ch not in template[i]:
                    continue
                letter_freq = letter_count_dict[ch][i]
                cur_word_sum += letter_freq

            if cur_word_sum > best_guess_sum:
                best_guess = word
                best_guess_sum = cur_word_sum
        print(best_guess)
        return best_guess

    def make_guess(self, guess):
        self.guesses_dict[guess] = self.result_rep(guess)
        self.number_attempts += 1

        if guess == self.secret_word:
            self.run_status = False

    def solve(self):
        while self.run_status == True:
            cur_guess = self.find_guess()
            self.make_guess(cur_guess)
            if self.number_attempts > 10:
                break
        return cur_guess

    def get_attempts(self):
        return self.number_attempts


game1 = Wordle(length=5, is_random_word=False, manual_index=2)
print(game1)
final_guess = game1.solve()
number_attempts = game1.get_attempts()
print(f"Solved for {final_guess} in {number_attempts}")
