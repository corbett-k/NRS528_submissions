# # CODING CHALLENGE 2
#
# # Coding Challenge 2.1: List Values
#
# # Using this list: [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
#
# # 1. Make a new list that has all the elements less than 5 from
# #    this list in it and print out this new list.

list1 = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
less_than_5 = []

for i in list1:
    if i < 5:
        less_than_5.append(i)
print(less_than_5)

# # 2. Write this in one line of Python (you do not need to append
# #    to a list just print the output).

list1 = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]

print([i for i in list1 if i < 5])
