from wordle_player import Wordle
import json

with open("words.json") as json_data:
    data = json.load(json_data)
    words_5 = data["5"]

solved_dict = {}
for i, word in enumerate(words_5):
    game = Wordle(length=5, is_random_word=False, manual_index=i)
    secret_word = game.get_secret_word()
    final_guess = game.solve()
    number_attempts = game.get_attempts()
    print(f"{secret_word} -> Solved for {final_guess} in {number_attempts} tries.")
    solved_dict[word] = i
