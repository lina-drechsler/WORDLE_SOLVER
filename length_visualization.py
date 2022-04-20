#The purpose of this file is to analyze the data (dictionary words)
#and create a visualization of which n-lettered words are most abundant

#imports
from matplotlib.pyplot import ply
import matplotlib.pyplot as plt

#clean up the data after scaraped (ignore dashes, spaces etc)

#count the lenghts using a dictionary
d = {}
for w in words:
    l = len(w)
    d[l] = d.get(l, 0) + 1

#retrieve into from the dictionary created
length, count = zip(*d.items())

#plot the n-lettered words and their counts
plt.bar(length, count)
plt.xticks(range(1, max(lengths)+1))
plt.xlabel('word lengths (in letters)')
plt.ylabel('word count')
plt.title('quanitity of n-lettered words in the dictionary')

plt.show()

