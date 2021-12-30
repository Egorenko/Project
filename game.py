import random


def name_input():  # ввод имени
    name = input('Enter your name: ')
    print(f'Hello, {name}')
    return name


def get_rating(name):
    with open('rating.txt', 'r') as game_rating:
        name_list = []
        score_list = []
        rating = 0
        line = game_rating.readline().rstrip()
        while line != '':
            name_list.append(line.split()[0])
            score_list.append(int(line.split()[1]))
            line = game_rating.readline().rstrip()
        score_dict = dict(zip(name_list, score_list))
        if name in score_dict:
            rating = score_dict[name]
        return rating


def get_options():
    choices_case = [i for i in input('').split(', ')]
    if choices_case == ['']:
        choices_case = ['rock', 'paper', 'scissors']
    print("Okay, let's start")
    return choices_case


def gamer_input(name, rating, choices_case):  # проверка ввода
    word = input()
    if word == '!exit':
        print('Bye!')
    elif word == '!rating':
        if rating != 0:
            print(f'Your rating: {rating}')
        else:
            rating = get_rating(name)
            print(f'Your rating: {rating}')
        return gamer_input(name, rating, choices_case)
    elif word in choices_case:
        return game(name, word, rating, choices_case)
    else:
        print('Invalid input')
        return gamer_input(name, rating, choices_case)


def game(name, gamer_choice, rating, choices_case):  # игра
    ai_choice = random.choice(choices_case)
    winning_cases = {
        'water': ['scissors', 'fire', 'rock', 'hun', 'lightning', 'devil', 'dragon'],
        'dragon': ['snake', 'scissors', 'fire', 'rock', 'gun', 'lightning', 'devil'],
        'devil': ['tree', 'human', 'snake', 'scissors', 'fire', 'rock', 'gun'],
        'gun': ['wolf', 'tree', 'human', 'snake', 'scissors', 'fire', 'rock'],
        'rock': ['sponge', 'wolf', 'tree', 'human', 'snake', 'scissors', 'fire'],
        'fire': ['paper', 'sponge', 'wolf', 'tree', 'human', 'snake', 'scissors'],
        'scissors': ['air', 'paper', 'sponge', 'wolf', 'tree', 'human', 'snake'],
        'snake': ['water', 'air', 'paper', 'sponge', 'wolf', 'tree', 'human'],
        'human': ['dragon', 'water', 'air', 'paper', 'sponge', 'wolf', 'tree'],
        'tree': ['devil', 'dragon', 'water', 'air', 'paper', 'sponge', 'wolf'],
        'wolf': ['lightning', 'devil', 'dragon', 'water', 'air', 'paper', 'sponge'],
        'sponge': ['gun', 'lightning', 'devil', 'dragon', 'water', 'air', 'paper'],
        'paper': ['rock', 'gun', 'lightning', 'devil', 'dragon', 'water', 'air'],
        'air': ['fire', 'rock', 'gun', 'lightning', 'devil', 'dragon', 'water'],
        'lightning': ['tree', 'human', 'snake', 'scissors', 'fire', 'rock', 'gun']
    }
    if ai_choice == gamer_choice:
        print(f'There is a draw ({ai_choice})')
        rating += 50
        return gamer_input(name, rating, choices_case)
    elif ai_choice in winning_cases[gamer_choice]:
        print(f'Well done. The computer chose {ai_choice} and failed')
        rating += 100
        return gamer_input(name, rating, choices_case)
    else:
        print(f'Sorry, but the computer chose {ai_choice}')
        return gamer_input(name, rating, choices_case)


gamer_name = name_input()
choices = get_options()
gamer_rating = get_rating(gamer_name)
gamer_input(gamer_name, gamer_rating, choices)
