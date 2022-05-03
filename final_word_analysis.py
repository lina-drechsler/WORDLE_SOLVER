# Hardest / Easiest Words to guess
import json

with open("guesses.json") as json_data:
    data = json.load(json_data)

hardest_words = {}
easiest_words = {}
lengths = ["3", "4", "5", "6", "7", "8", "9", "10"]
for length in lengths:
    guesses = data[length]
    cur_hard_word = ""
    cur_hard_guesses = 0
    cur_easy_word = ""
    cur_easy_guesses = 100
    for word, num_guess in guesses.items():
        if type(num_guess) is list:
            continue
        if num_guess > cur_hard_guesses:
            cur_hard_guesses = num_guess
            cur_hard_word = word
        if num_guess < cur_easy_guesses:
            cur_easy_guesses = num_guess
            cur_easy_word = word
    hardest_words[length] = (cur_hard_word, cur_hard_guesses)
    easiest_words[length] = (cur_easy_word, cur_easy_guesses)

print(f"hardest: {hardest_words}")
print(f"easiest: {easiest_words}")
