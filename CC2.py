# # CODING CHALLENGE 2
#
# # Coding Challenge 2.1: List Values
#
#
# # Coding Challenge 2.2: List Overlap
#
# list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
# list_b = ['dog', 'hamster', 'snake']
#
# in_both = [element for element in list_a if element in list_b]
# print(in_both)
#
# not_in_both = [element for element in list_a if element not in list_b]
# print(not_in_both)
#
#
# # Coding Challenge 2.3: Count Occurrences of Words in a Phrase
#
# def word_count(str):
#     counts = dict()
#     words = str.split()
#     for word in words:
#             if word in counts:
#                 counts[word] += 1
#             else:
#                 counts[word] = 1
#     return counts
# print(word_count('hi dee hi how are you mr dee'))
#
#
# # Coding Challenge 2.4: User Input
#
# age = input("What is your age? ")
# print("Your age is " + str(age))
# age_til_65 = 65 - int(age)
# print("You will be 65 in " + str(age_til_65))


# Coding Challenge 2.5: User Input 2



letter_scores = {
    "aeioulnrst": 1,
    "dg": 2,
    "bcmp": 3,
    "fhvwy": 4,
    "k": 5,
    "jx": 8,
    "qz": 10
}
