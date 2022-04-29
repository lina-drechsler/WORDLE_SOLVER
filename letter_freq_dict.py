# Function returns a dictionary that sums the character counts for all words of specified lengths
# parameters: n = word length
def let_freq_dic_generator(n):

    # n-letter words dictionary with all 26 alphabetical letters
    n_letter_words = {
        "a": [],
        "b": [],
        "c": [],
        "d": [],
        "e": [],
        "f": [],
        "g": [],
        "h": [],
        "i": [],
        "j": [],
        "k": [],
        "l": [],
        "m": [],
        "n": [],
        "o": [],
        "p": [],
        "q": [],
        "r": [],
        "s": [],
        "t": [],
        "u": [],
        "v": [],
        "w": [],
        "x": [],
        "y": [],
        "z": [],
    }

    # Initialize list values to 0 based on the word lengths. Length 3 ex: [0, 0, 0]
    for letter, _ in n_letter_words.items():
        n_letter_words[letter] = [0 for _ in range(n)]

    # Loop through all words of specified n length and add the character count to the accumulator list
    with open(f"./data/{n}.txt", "r") as f:
        lines = f.readlines()
        for word in lines:
            word = word.rstrip()
            for (i, letter) in enumerate(word):
                n_letter_words[letter][i] += 1

    return n_letter_words


# Run the let_freq_dic_generator function on word lengths 3 to 10 (inclusive)
all_lengths = [3, 4, 5, 6, 7, 8, 9, 10]
all_counts = {}

for length in all_lengths:
    all_counts[length] = let_freq_dic_generator(length)

# Write the counts to a JSON file to easily access the values later
import json

with open("counts.json", "w") as json_file:
    json.dump(all_counts, json_file)
