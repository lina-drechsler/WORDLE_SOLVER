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
            # for i, target_ch in range(len(target_rep)):
            # print(f"target_rep index: {i}")
            # print(f"guess_rep: {guess_rep}")
            guess_ch = guess_rep[i]
            # target_ch = target_rep[i]

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
        """
        Returns a dictionary template of a word that the solver could use as a guess for each character
        in each position based on information from previous guesses
        """
        # Initialize the template dictionary with the key as the word character index and value as an empty list
        template = {}
        for i in range(self.length):
            template[i] = []

        # Find all the correct letters/correct positions for the template
        # If its a correct match (result rep. = 2), replace the value list with just that letter
        for word, rep in self.guesses_dict.items():
            for i, ch in enumerate(word):
                if rep[i] == 2:
                    template[i] = [ch]

        # Second, find all the correct letters/incorrect positions for the template
        for word, rep in self.guesses_dict.items():
            for i, ch in enumerate(word):
                if rep[i] == 1:
                    # Add letter to incorrect_positions dictionary
                    self.incorrect_positions[i].add(ch)

                    for j, values in template.items():
                        # If the character is in the template at that position, get rid of the character from that position's template
                        if ch in values:
                            ch_index = template[j].index(ch)
                            template[j].pop(ch_index)
                        # Add letter to the template for all other positions as long as (must satisfy all three conditions):
                        # - Character isn't at the index where rep[i] == 1 (i.e. the same position that was correct letter/incorrect position)
                        # - The representation of that index isn't 2 (i.e. already a correct letter/position)
                        # - The character isn't in values of the incorrect_positions at that index
                        if (
                            j != i
                            and rep[j] != 2
                            and ch not in self.incorrect_positions[j]
                        ):
                            template[j].append(ch)

        # Add all the incorrect letters to the incorrect_letters list
        for word, rep in self.guesses_dict.items():
            for i, ch in enumerate(word):
                if rep[i] == 0:
                    self.incorrect_letters.append(ch)

        return template

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

    # def word_entropy(self, word):
    #     """
    #     Returns the entropy of the word based off of character position
    #     Parameters: word = the word to check the characters of
    #     """
    #     with open("counts.json") as json_data:
    #         data = json.load(json_data)
    #         letter_count_dict = data[str(self.length)]

    #     count = 0
    #     for i, ch in enumerate(word):
    #         count += letter_count_dict[ch][i]
    #     return round(count / (len(word) - len(set(word)) + 1))

    # from scipy.stats import entropy
    # # Initialize probability list
    # prob_list = []
    # # Get current template
    # temp_template = self.make_template()
    # # Get current represenation
    # cur_rep = [(guess, rep) for (guess, rep) in self.guesses_dict.items()][-1][1]
    # for i, ch in enumerate(word):
    #     if cur_rep[i] == 2:
    #         continue

    # chars = len(word)
    # dim = 0
    # while dim < chars:
    #     for ch in word[dim:chars]:
    #     dim += 1

    # word_entropy = entropy(prob_list, base=2)
    # return word_entropy

    # def calculate_commonalities(self, possible_guesses):
    #     """
    #     Returns a dictionary of the entropies for each possible guess
    #     Parameter: possible guesses = a list of guesses that could be a potential answer
    #     """
    #     # from scipy.stats import entropy
    #     # Initialize the dictionary
    #     commonality_dict = {}
    #     for guess in possible_guesses:
    #         # Use entropy calculation
    #         score = self.word_commonality(guess)
    #         # Add the entropy to the dictionary
    #         commonality_dict[guess] = score
    #     return commonality_dict

    def find_guesses(self):
        """
        Updates the list of potential guesses based off the current character template
        """
        # Get the word template that will be used to find potential guesses
        template = self.make_template()
        # print(template)
        cur_rep = self.get_current_rep()
        # print(cur_rep)

        possible_guesses = []
        # Loop through all words to find possible words
        for word in self.possible_words:
            # Loop through the index, character in each word
            for i, ch in enumerate(word):
                # Go to next word if the character is in the incorrect_letters list
                if ch in self.incorrect_letters:
                    continue
                # Go to next word if the character is in the values of incorrect_positions at that index
                elif ch in self.incorrect_positions[i]:
                    continue
                # If the letter is already correct make sure it is there
                elif cur_rep[i] == 2 and ch not in template[i]:
                    continue
                # Add the word to the possible_guesses list if it passes previous two conditions
                else:
                    possible_guesses.append(word)
        # Should possible_guesses replace self.possible_words ???? *********************
        self.possible_words = possible_guesses
        return possible_guesses

    def get_best_guess(self):
        """
        Returns the guess with the highest entropy, i.e. the best next guess
        Parameter: entropies = dictionary of possible guesses as values and entropy values
        """
        cur_rep = self.get_current_rep()
        last_guess = self.get_last_guess()

        best_word = ""
        best_entropy = 0
        for word in self.possible_words:
            seen_chars = set()
            number_greens = 0
            number_yellows = 0
            total_count = 0
            for i, ch in enumerate(word):
                # print(f"cur_rep: {cur_rep}")
                # print(f"last_guess: {last_guess}")
                # print(f"word_loop: {word}")
                # print(f"word_loop index: {i}")
                # print(f"word_loop ch: {ch}")
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

        # # Set the base condition
        # guesses = [word for word, _ in commonality_dict.items()]
        # best_guess = guesses[0]
        # best_guess_comm = commonality_dict[best_guess]

        # # Loop through commonality values to find the highest value
        # for guess in guesses[1:]:
        #     cur_comm = commonality_dict[guess]
        #     if cur_comm > best_guess_comm:
        #         best_guess_comm = cur_comm
        #         best_guess = guess

        # return best_guess

    def make_guess(self, guess):
        """
        Make the guess and update varaibles based on the guess.
        Parameter: guess = the guessed hidden word being made
        """
        # Add the guess and it's resulting represnation to the guesses_dict
        self.guesses_dict[guess] = self.result_rep(guess)
        # Increase the number of attempts
        self.number_attempts += 1
        # Remove that guess from the list of possible_words
        self.possible_words.remove(guess)
        # Update the template
        self.make_template()
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
            self.find_guesses()
            cur_guess = self.get_best_guess()
            print(cur_guess)
            self.make_guess(cur_guess)
            print("Made a guess")
        return cur_guess
