import random

target = random.randint(1, 9)

while True:
    guess = int(input("Guess a number between 1 and 9: "))
    if guess == target:
        print("Well guessed!")
        break
    else:
        print("Wrong guess, try again!")