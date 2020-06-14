# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import random
answer = random.randint(1, 100)
rules = 'I\'m thinking of a number between 1 and 100. \nPick a number between 1 and 100. \nIf your first guess is within 10 you will be told WARM, but if not you will be told COLD. \nIf your next guess is closer the prompt will be WARMER, but if not it will be colder'
print (rules)



# %%
guesses = [0]


# %%
while True:

    guess = int(input('I\'m thinking of a number between 1 and 100. What is it? '))

    if guess < 1 or guess > 100:
        print('OUT OF BOUNDS! Please try again: ')
        continue

    elif guess == answer:
        print('Awwwww you got me! The number I was thinking of was ' + str(answer))
        break

    elif guess != answer:
        guesses = guesses + [guess]
        if len(guesses) == 2 and abs(answer-guess) > 10:
            print('COLD')
            print('I\'m thinking of a number between 1 and 100. What is it? ')
        elif len(guesses) == 2 and abs(answer-guess) <= 10:
            print('WARM')
        elif len(guesses) > 2 and (abs(answer-guesses[-2]) > abs(answer-guesses[-1])):
            print('WARMER')
        elif len(guesses) > 2 and (abs(answer-guesses[-2]) < abs(answer-guesses[-1])):
            print('COLDER')
            continue
        else:
            print(guesses)
            print('ERROR')
            
            break


# %%


