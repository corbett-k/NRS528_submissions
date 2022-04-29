# # CODING CHALLENGE 2
#
# # Coding Challenge 2.4: User Input
#
# # Ask the user for an input of their current age, and tell them how many years until
# # they reach retirement (65 years old).

age = input("\nHow old are you? ")
print("\nYour age is " + str(age))

age_til_65 = 65 - int(age)
print("\nYou will be 65 in " + str(age_til_65) + " years.")
