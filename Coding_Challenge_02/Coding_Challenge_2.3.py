# # CODING CHALLENGE 2
#
# # Coding Challenge 2.3: Given a single phrase, count the occurrence of each word
#
# # Using this string: 'hi dee hi how are you mr dee'
# # Count the occurrence of each word, and print the word plus the count
# # (hint, you might want to "split" this into a list by a white space: " ").

def word_count(string_a):
    count = dict()
    words = string_a.split()
    for i in words:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    return count


print(word_count('hi dee hi how are you mr dee'))
