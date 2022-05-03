from wordle_player import Wordle
import json
from random import shuffle


def get_solve_dict(length):
    # with open("words.json") as json_data:
    #     data = json.load(json_data)
    #     words = data[length]

    solved_dict = {}
    indices = [num for num in range(0, 50)]
    shuffle(indices)
    for i in indices:
        # print(i)
        game = Wordle(length=int(length), is_random_word=False, manual_index=i)
        secret_word = game.get_secret_word()
        print(game)
        final_guess = game.solve()
        number_attempts = game.get_attempts()
        print(f"{secret_word} -> Solved for {final_guess} in {number_attempts} tries.")
        solved_dict[secret_word] = number_attempts
    return solved_dict


def main():
    # lengths = ["4", "5", "6", "7", "8", "9", "10"]
    lengths = ["5"]
    word_guess_dict = {}
    average_guess_dict = {}
    for length in lengths:
        solved_dict = get_solve_dict(length)
        word_guess_dict[length] = solved_dict
        sum_guesses = sum([num_guesses for _, num_guesses in solved_dict.items()])
        avg_guess = sum_guesses / len(solved_dict)
        average_guess_dict[length] = avg_guess

    import json

    with open("guesses.json", "w") as json_file:
        json.dump(word_guess_dict, json_file, indent=4)

    with open("averages.json", "w") as json_file:
        json.dump(average_guess_dict, json_file, indent=4)


if __name__ == "__main__":
    main()
