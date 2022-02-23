# # CODING CHALLENGE 2
#
# # Coding Challenge 2.2: List Overlap
#
# # Using these lists:

list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']

# 1. Determine which items are present in both lists.

print(str([i for i in list_a if i in list_b]) + ' are on both lists.')

# 2. Determine which items do not overlap in the lists.

print(str([i for i in list_a if i not in list_b]) + ' do not appear in both lists.')
