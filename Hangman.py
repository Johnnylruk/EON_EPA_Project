import random as rd

word_list = ['aardvark', 'baboon','camel']
chosen_word = rd.choice(word_list)
print(chosen_word)
place_holder = ''

for letter in chosen_word:
    place_holder += '_' 
print(place_holder)

correct_letters = []

while True:
    
    guess_letter = str(input('Guess a letter: ')).strip().lower()

    display = ''

    for letter in chosen_word:
        if letter == guess_letter:
            display += letter
            correct_letters.append(guess_letter)
        elif letter in correct_letters:
            display += letter
        else:
            display += '_'
    print(display)

    if '_' not in display:
        print('You win.')
        break
