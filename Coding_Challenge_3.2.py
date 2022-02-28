# Coding Challenge 3.2: Push sys.argv to the limit

# Construct a rudimentary Python script that takes a series of inputs as a command from a bat file using sys.argv,
# and does something to them. The rules:
# 1. Minimum of three arguments to be used.
# 2. You must do something simple in 15 lines or less within the Python file.
# 3. Print or file generated output should be produced.

import sys #1
def main(arg): #2
    print("\nThe closest planet to the sun is " + str(arg) + ".") #3
main(sys.argv[1]) #4
def main(arg): #5
    print("\nThe second closest planet to the sun is " + str(arg) + ".") #6
main(sys.argv[2]) #7
def main(arg): #8
    print("\nThe third closest planet to the sun is " + str(arg) + ".") #9
main(sys.argv[3]) #10
def main(arg): #11
    print("\nThe fourth closest planet to the sun " + str(arg) + ".") #12
main(sys.argv[4]) #13