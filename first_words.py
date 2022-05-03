from wordle_player import Wordle

lengths = ["3", "4", "5", "6", "7", "8", "9", "10"]

best_first_words = {}
for length in lengths:
    game = Wordle(length=int(length))
    first_guess = game.find_first_guess()
    best_first_words[int(length)] = first_guess


import json

with open("first_guesses.json", "w") as json_file:
    json.dump(best_first_words, json_file, indent=4)
