# # CODING CHALLENGE 2
# # Coding Challenge 2.5: User Input 2

letter_scores = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1,  "f": 4,
                 "g": 2, "h": 4, "i": 1, "j": 8, "k": 5,  "l": 1,
                 "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1,
                 "s": 1, "t": 1, "u": 1, "v": 4, "w": 4,  "x": 8,
                 "y": 4, "z": 10}

def scrabble_word_count(word):
    result = 0
    for letter in word:
        result += letter_scores[letter]
    return result

word = input("Enter a word you would like scored in Scrabble: ")
word_score = scrabble_word_count(word)

print("\n" + "'" + word.title() + "'" + " is worth " + str(word_score) + " points in scabble.")
