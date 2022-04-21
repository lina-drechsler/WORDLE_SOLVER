############################    ############################
############################    ############################
### DO NOT RUN THIS FILE ###    ### DO NOT RUN THIS FILE ###
############################    ############################
############################    ############################

# Takes the data from words_alpha.txt and organizes the words into .txt files based on word length

# Step 1: Get all the data into a dictionary
file = "./data/words_alpha.txt"

all_words = {}
with open(file, "r") as f:

    lines = f.readlines()
    for word in lines:
        word = word.rstrip()
        word_len = len(word)
        if word_len not in all_words:
            all_words[word_len] = []
        all_words[word_len].append(word)

# Step 2: Only include word lengths between 5 and 14 (inclusive)
keys = list(all_words.keys())
for key in keys:
    if key < 5 or key > 14:
        all_words.pop(key)
    else:
        continue

# Step 3: Write the words of each length to their respective .txt files
for word_len, words in sorted(all_words.items()):
    path = f"./data/{word_len}.txt"
    with open(path, "a") as f:
        for word in words:
            f.write(f"{word}\n")

############################    ############################
############################    ############################
### DO NOT RUN THIS FILE ###    ### DO NOT RUN THIS FILE ###
############################    ############################
############################    ############################
