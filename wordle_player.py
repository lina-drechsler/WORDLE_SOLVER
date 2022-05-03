
from random import randint
import json
from scipy.stats import entropy

# Defining the Wordle class that will contain game rules and the solving algorithm
class Wordle:
    def __init__(self, length=5, is_random_word=True, manual_index=0):
        """
        Intializing function for a Wordle object.
        Parameters: length = the desired length of the Wordle game
        is_random_word = True (the automatic value): if you would like to play the game with a random word
            False: if you want to specify the index of the secret_word
        manual_index (0)= if is_random_word is False, the index of the secret_word in the words.json file of size self.length
        """
        self.length = length
        self.is_random_word = is_random_word
        self.manual_index = manual_index
        # Set the secret_word based on if you want it to be random or indexed
        if is_random_word:
            self.secret_word = self.set_word()
        else:
            self.secret_word = self.set_word(manual_index)
        # True when the secret_word has not been found, false if it's found and the game has ended
        self.run_status = True
        # Keeps track of guesses
        self.number_attempts = 0
        # Keeps track of letters not in the word
        self.incorrect_letters = []
        # Keeps track of letters not in a specific index of the word
        self.incorrect_positions = {x: set() for x in range(self.length)}
        # Keeps track of correct letters of the word
        self.correct_positions = {x: set() for x in range(self.length)}
        # Keeps track of incorrect positions list
        self.incorrect_positions_list = []
        # Keeps track of the Wordle guesses
        # Key: guessed word
        # Value: guessed word representation
        self.guesses_dict = {}
        # Load the words of self.length into a list of possible hidden_words
        with open("words.json") as json_data:
            data = json.load(json_data)
            self.possible_words = data[str(self.length)]

    def __repr__(self):
        """
        Print the hidden word when the print() function is called on a Wordle object
        """
        return f"The word is: {self.secret_word}"

    def get_attempts(self):
        """
        Returns the number of guesses that the game has placyed. Helper function.
        """
        return self.number_attempts

    def get_secret_word(self):
        """
        Returns the secret word of the game. Helper function.
        """
        return self.secret_word

    def get_last_guess(self):
        """
        Returns the  most recent guess.
        """
        return [(guess, rep) for (guess, rep) in self.guesses_dict.items()][-1][0]

    def get_current_rep(self):
        """
        Returns the represenation for most recent guess.
        """
        return [(guess, rep) for (guess, rep) in self.guesses_dict.items()][-1][1]

    def set_word(self, manual_index=0):
        """
        Returns a random word of size self.length to be used as the secret word.
        Parameters: manual_index = the index of the word in the words.json file of size self.length
        """
        # Set the word when a random word is requested and an index is provided
        if self.is_random_word == False:
            with open("words.json") as json_data:
                data = json.load(json_data)
            return data[str(self.length)][manual_index]

        # Set the word to a random word when a random word is requested
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
        Parameters: guess = the guessed word to create the resulting representation

        Correct Letter/Correct Position: 2
        Correct Letter/Wrong Position: 1
        Wrong Letter/Wrong Position: 0
        """
        # Make the reprentation of the secret_word. Ex. "steam": ['s', 't', 'e', 'a', 'm']
        target_rep = [ch for ch in self.secret_word]
        # print(target_rep)
        # Count the characters in the hidden word with a character key and character count value
        target_ch_count = {}
        for ch in target_rep:
            if ch not in target_ch_count:
                target_ch_count[ch] = 0
            target_ch_count[ch] += 1

        # Make the reprentation of the guess. Ex. "steam": ['s', 't', 'e', 'a', 'm']
        guess_rep = [ch for ch in guess]

        # Intialize final representation
        final_rep = []
        # Assign all 2's (correct letter/correct position)
        for i, target_ch in enumerate(target_rep):
            guess_ch = guess_rep[i]

            if target_ch == guess_ch:
                final_rep.append(2)
                target_ch_count[guess_ch] -= 1
                self.correct_positions[i].add(guess_ch)
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
                    self.incorrect_positions[i].add(guess_ch)
                    self.incorrect_positions_list.append(guess_ch)
                else:
                    self.incorrect_letters.append(guess_ch)
        return final_rep

    def word_in_rep(self, cur_word, rep, last_guess):
        """
        Returns True if the word fits in the representation, else returns False
        """
        # First check for 2s
        for i, num in enumerate(rep):
            if num == 2:
                if cur_word[i] != last_guess[i]:
                    return False
        # Then check for 1s
        for i, num in enumerate(rep):
            if num == 1:
                if last_guess[i] not in cur_word or last_guess[i] == cur_word[i]:
                    return False
        # Last check for 0s
        for i, ch in enumerate(cur_word):
            if ch in self.incorrect_letters:
                return False

        return True

    def find_first_guess(self):
        """
        Returns the "optimal" first guess based on the character frequency per position
        """
        # Opens the counts dictionary to begin counting positions
        with open("counts.json") as json_data:
            data = json.load(json_data)
            letter_count_dict = data[str(self.length)]

        # Set the Baseline Guess
        best_first_guess = self.possible_words[0]
        best_guess_sum = 0
        for i, ch in enumerate(best_first_guess):
            letter_freq = letter_count_dict[ch][i]
            best_guess_sum += letter_freq

        # Loop through all words to find possible words
        for word in self.possible_words[1:]:
            cur_word_sum = 0
            letter_freq = letter_count_dict[ch][i]
            cur_word_sum += letter_freq

            if cur_word_sum > best_guess_sum:
                best_first_guess = word
                best_guess_sum = cur_word_sum
        return best_first_guess

    def find_guesses(self):
        """
        Updates the list of potential guesses based off the current character template
        """
        # Get the word template that will be used to find potential guesses
        cur_rep = self.get_current_rep()
        last_guess = self.get_last_guess()

        possible_guesses = [word for word in self.possible_words]

        # Loop through all words to find possible words
        for word in self.possible_words:
            if self.word_in_rep(word, cur_rep, last_guess) == True:
                continue
            else:
                possible_guesses.remove(word)

        # Update the possible words
        self.possible_words = [word for word in possible_guesses]
        return possible_guesses

        # # Checks for a previous guess
        # if word in [guess for guess, _ in self.guesses_dict.items()]:
        #     possible_guesses.remove(word)
        # # Checks to make sure that the word contains a letter if it's in the wrong position earlier
        # word_rep = [ch for ch in word]
        # incorrect_pos_tracker = True
        # for pos, letter_set in self.incorrect_positions.items():
        #     if len(letter_set) > 0:
        #         for ch in letter_set:
        #             if ch not in word_rep:
        #                 incorrect_pos_tracker = False
        # if incorrect_pos_tracker == False:
        #     try:
        #         possible_guesses.remove(word)
        #         continue
        #     except:
        #         continue
        # # Loop through the index, character in each word
        # good_word = True
        # for i, ch in enumerate(word):
        #     # Go to next word if the character is in the incorrect_letters list
        #     if ch in self.incorrect_letters:
        #         good_word = False
        #         try:
        #             possible_guesses.remove(word)
        #         except:
        #             continue
        #     # Go to next word if the character is in the values of incorrect_positions at that index
        #     elif ch in self.incorrect_positions[i]:
        #         good_word = False
        #         try:
        #             possible_guesses.remove(word)
        #         except:
        #             continue
        #     # If the letter is already correct make sure it is there
        #     elif cur_rep[i] == 2 and word[i] != ch:
        #         good_word = False
        #         try:
        #             possible_guesses.remove(word)
        #         except:
        #             continue
        # self.possible_words = possible_guesses
        # return possible_guesses

    def get_best_guess(self, possible_guesses):
        """
        Returns the guess with the highest entropy, i.e. the best next guess
        Parameter: entropies = dictionary of possible guesses as values and entropy values
        """
        cur_rep = self.get_current_rep()
        last_guess = self.get_last_guess()

        best_word = possible_guesses[0]
        best_entropy = 0
        for word in possible_guesses[1:]:
            seen_chars = set()
            number_greens = 0
            number_yellows = 0
            total_count = 0
            for i, ch in enumerate(word):

                if cur_rep[i] == 2:
                    if last_guess[i] == ch:
                        number_greens += 1
                        total_count += 1
                elif cur_rep[i] == 1:
                    if ch not in seen_chars:
                        if last_guess[i] == ch:
                            number_yellows += 1
                            total_count += 1
                        seen_chars.add(ch)
                else:
                    total_count += 1
            number_grays = total_count - number_greens - number_yellows
            total = number_greens + number_yellows + number_grays
            dist = [number_greens / total, number_yellows / total, number_grays / total]
            cur_entropy = entropy(dist, base=2)

            if cur_entropy > best_entropy:
                best_entropy = cur_entropy
                best_word = word

        return best_word

    def make_guess(self, guess):
        """
        Make the guess and update varaibles based on the guess.
        Parameter: guess = the guessed hidden word being made
        """
        # Add the guess and it's resulting represnation to the guesses_dict
        self.guesses_dict[guess] = self.result_rep(guess)
        # print(self.guesses_dict)
        # Increase the number of attempts
        self.number_attempts += 1
        # Remove that guess from the list of possible_words
        self.possible_words.remove(guess)
        # If the hidden_word is found, change the run_status to False as the game has been completed.
        if guess == self.secret_word:
            self.run_status = False

    def solve(self):
        """
        Returns the solved final word of the Wordle game.
        """
        # Make the first guess
        first_guess = self.find_first_guess()
        self.make_guess(first_guess)
        # Make the  guesses while the game is running
        while self.run_status == True:
            possible_guesses = self.find_guesses()
            cur_guess = self.get_best_guess(possible_guesses)
            print(cur_guess)
            self.make_guess(cur_guess)
            print("Made a guess")
        return cur_guess
