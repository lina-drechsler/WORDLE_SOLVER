# Takes the data from words_alpha.txt and organizes the words into .txt files based on word length

# Step 1: Get all the data into a dictionary
file = "./data/words_alpha1.txt"

all_words = {}
with open(file, "r") as f:

    lines = f.readlines()
    for word in lines:
        word = word.rstrip()
        word_len = len(word)
        if word_len not in all_words:
            all_words[word_len] = []
        all_words[word_len].append(word)

# Step 2: Only include word lengths between 3 and 10 letters (inclusive)
keys = list(all_words.keys())
for key in keys:
    if key < 3 or key > 10:
        all_words.pop(key)
    else:
        continue

# Step 3: Write the words of each length to their respective .txt files
for word_len, words in sorted(all_words.items()):
    path = f"./data/{word_len}.txt"
    with open(path, "w") as f:
        for word in words:
            f.write(f"{word}\n")

# Step 4: Write all the words to a JSON File
import json

with open("words.json", "w") as json_file:
    json.dump(all_words, json_file)
