# imports
import matplotlib.pyplot as plt
import json

with open("averages.json") as json_data:
    data = json.load(json_data)

lengths = []
average_guesses = []

for length, avg_guess in data.items():
    lengths.append(length)
    average_guesses.append(avg_guess)

# plot the average guesses
plt.bar(lengths, average_guesses)
plt.xlabel("word lengths (in letters)")
plt.ylabel("average number of guesses")
plt.title("average guess distribution for word lengths")

plt.show()
