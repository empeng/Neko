import sys
import re
import numpy

rainbow = set(["red", "green", "blue", "yellow", "orange", "purple"])
file_name = sys.argv[1]

def entropy(dist, axis=None):
    return -numpy.sum(dist * numpy.nan_to_num(numpy.log(dist)), axis)

unique_words = set()
color_by_word_counts = {}
for line in open(file_name):

    # clean punctuation
    line = re.sub(r"[^a-zA-Z]", " ", line)

    # lower case and split line
    words_in_line = line.lower().split()

    for color in [word for word in words_in_line if word in rainbow]:
        for associated_word in [word for word in words_in_line if word != color]:            
            unique_words.add(associated_word)
            color_by_word_counts[color] = color_by_word_counts.get(color, {})
            color_by_word_counts[color][associated_word] = color_by_word_counts[color].get(associated_word, 0) + 1


num_colors = len(color_by_word_counts)
vocab_size = len(unique_words)
print num_colors, vocab_size

color_word_matrix = numpy.zeros(shape=(num_colors, vocab_size))

color_index_lookup = {color:number for number, color in enumerate(color_by_word_counts.keys())}
index_color_lookup = {index:color for color, index in color_index_lookup.iteritems()}


word_index_lookup = {word:number for number, word in enumerate(unique_words)}  
index_word_lookup = {index:word for word, index in word_index_lookup.iteritems()}

for color, word_counts in color_by_word_counts.iteritems():
    for word, word_count in word_counts.iteritems():
        color_word_matrix[color_index_lookup[color]][word_index_lookup[word]] = word_count

#convert counts to proportions
color_word_matrix_proportions = numpy.transpose(color_word_matrix.T / color_word_matrix.sum(1))

scores = []
for word_id, (word_proportions, word_counts) in enumerate(zip(color_word_matrix_proportions.T, color_word_matrix.T)):
    word_proportions /= word_proportions.sum()
    word = index_word_lookup[word_id]
    scores.append((entropy(word_proportions), word_counts.sum(), word, word_counts))

for word, word_counts in [(word, word_counts) for ent, count, word, word_counts in sorted(scores) if count > 3][0:20]:
    print word, " ".join(["%s:%d" % (index_color_lookup[i], x) for i, x in enumerate(word_counts) if x > 0])

