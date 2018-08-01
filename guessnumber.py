# uess a random number from 1 to 100 in 7 maximum attempts

import random

number = random.randint(1, 101)
print('Guess a random number from 1 to 100 in 7 guesses!')
print()

attempts = 7

while attempts > 0:
    guess = int(input("Num: "))
    
    if guess == number:
        print("\n- Right Guess! -")
        break
    elif guess > number:
        print("Guess lower!")
    else:
        print("Guess higher!")

    attempts -= 1

else:
    print('\n- No more guesses! -')
