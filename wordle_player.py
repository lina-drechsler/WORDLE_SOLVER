from random import randint
import json

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

        # Get the word template that will be used to find potential guesses
        # template = self.make_template()

        # Loop through all words to find possible words
        for word in self.possible_words[1:]:
            cur_word_sum = 0
            for i, ch in enumerate(word):
                # if ch in self.incorrect_letters:
                #     continue
                # I'm not sure if this condition is neccessary......
                # elif len(template[i]) > 0 and ch not in template[i]:
                #     continue
                # elif ch in self.incorrect_positions[i]:
                #     continue
                # else:
                letter_freq = letter_count_dict[ch][i]
                cur_word_sum += letter_freq

            if cur_word_sum > best_guess_sum:
                best_first_guess = word
                best_guess_sum = cur_word_sum
        return best_first_guess

    def find_guesses(self):
        """
        Returns a list of potential guesses based off the current character template
        """
        # Get the word template that will be used to find potential guesses
        # NOT SURE IF THIS IS NEEDED
        template = self.make_template()

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
                # Add the word to the possible_guesses list if it passes previous two conditions
                else:
                    possible_guesses.append(word)
        # Should possible_guesses replace self.possible_words ???? *********************
        return possible_guesses

    def calculate_entropies(self, possible_guesses):
        """
        Returns a dictionary of the entropies for each possible guess
        Parameter: possible guesses = a list of guesses that could be a potential answer
        """
        # Initialize the dictionary
        entropies = {}
        for guess in possible_guesses:
            # Make a temporary template for this guess

            # Find the words that fit into this temporary template

            # Caluclate the length of the template
            # Calculate the current gueses entropy
            entropy = 0
            # Add the entropy to the dictionary
            entropies[guess] = entropy
        return entropies

    def get_best_guess(self, entropies):
        """
        Returns the guess with the highest entropy, i.e. the best nextt guess
        Parameter: entropies = dictionary of possible guesses as values and entropy values
        """
        # Set the base condition
        guesses = [word for word, _ in entropies.items()]
        best_guess = guesses[0]
        best_guess_entropy = entropies[best_guess]

        # Loop through entropies to find the highest value
        # OR, choose the word with the shortest length of possible words
        for guess in guesses[1:]:
            cur_entropy = entropies[guess]
            if cur_entropy > best_guess_entropy:
                best_guess_entropy = cur_entropy
                best_guess = guess

        return best_guess

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
        # If the hidden_word is found, change the run_status to False as the game has been completed.
        if guess == self.secret_word:
            self.run_status = False

    def solve(self):
        """
        Returns the solved final word of the Wordle game.
        """
        # Initialize the first guess
        cur_guess = self.find_first_guess()
        self.make_guess(cur_guess)
        # Make the proceeding guesses while the game is running
        while self.run_status == True:
            possible_guesses = self.find_guesses()
            entropies = self.calculate_entropies(possible_guesses)
            cur_guess = self.get_best_guess(entropies)
            self.make_guess(cur_guess)
        return cur_guess
