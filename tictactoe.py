import random


class Table(list):  # игровое поле изначально пустое
    def __init__(self):
        super().__init__()
        self.table = [[' ' for _ in range(3)] for _ in range(3)]

    def print_table(self):
        print('---------')
        for i in range(3):
            print('|', *self.table[i], '|', sep=' ')
        print('---------')

    def game_over(self):  # проверка на конец игры
        for i in range(3):  # победа по горизонтали
            if self.table[i][0] != ' ' and self.table[i] == [self.table[i][0] for _ in range(3)]:
                return f'{self.table[i][0]} wins'
        for i in range(3):  # победа по вертикали
            if (self.table[0][i] != ' '
                    and self.table[0][i] == self.table[1][i]
                    and self.table[1][i] == self.table[2][i]):
                return f'{self.table[0][i]} wins'
        if self.table[0][0] != ' ' and all(self.table[0][0] == self.table[i][i] for i in range(1, 3)):
            return f'{self.table[0][0]} wins'  # победа по главной диагонали
        if self.table[0][2] != ' ' and all(self.table[0][2] == self.table[i][2 - i] for i in range(1, 3)):
            return f'{self.table[0][2]} wins'  # победа по побочной диагонали
        not_empty = True
        for line in self.table:
            if ' ' in line:
                not_empty = False
        if not_empty:
            return 'Draw'  # ничья

    def valid_coordinates(self, char):
        coordinates = input('Enter the coordinates: ')
        if coordinates[0].isdigit() and coordinates[2].isdigit():
            if 1 <= int(coordinates[0]) <= 3 and 1 <= int(coordinates[2]) <= 3:
                if self.table[int(coordinates[0]) - 1][int(coordinates[2]) - 1] == ' ':
                    self.table[int(coordinates[0]) - 1][int(coordinates[2]) - 1] = char
                    self.print_table()
                    return True
                else:
                    print('This cell is occupied! Choose another one!')
            else:
                print('Coordinates should be from 1 to 3!')
        else:
            print('You should enter numbers!')
        self.valid_coordinates(char)

    def randomize_coordinates(self, char, name):
        line = random.randint(0, 2)
        col = random.randint(0, 2)
        if self.table[line][col] == ' ':
            print(f'Making move level "{name}"')
            self.table[line][col] = char
            self.print_table()
            return True
        else:
            self.randomize_coordinates(char, name)

    def winner_or_scam_coordinates(self, char, name):
        un_char = 'X' if char == 'O' else 'O'
        for num, line in enumerate(self.table):  # по горизонтали
            if (line == [char, char, ' ']
                    or line == [char, ' ', char]
                    or line == [' ', char, char]):
                self.table[num][line.index(' ')] = char
                print(f'Making move level "{name}"')
                self.print_table()
                return True
            elif (line == [un_char, un_char, ' ']
                  or line == [un_char, ' ', un_char]
                  or line == [' ', un_char, un_char]):
                self.table[num][line.index(' ')] = char
                print(f'Making move level "{name}"')
                self.print_table()
                return True
        for i in range(3):  # по вертикали
            if (self.table[0][i] == char or self.table[0][i] == un_char) and self.table[1][i] == self.table[0][i] and \
                    self.table[2][i] == ' ':
                self.table[2][i] = char
                print(f'Making move level "{name}"')
                self.print_table()
                return True
            elif ((self.table[1][i] == char or self.table[0][i] == un_char)
                  and self.table[2][i] == self.table[1][i]
                  and self.table[0][i] == ' '):
                self.table[0][i] = char
                print(f'Making move level "{name}"')
                self.print_table()
                return True
            elif ((self.table[0][i] == char or self.table[0][i] == un_char)
                  and self.table[2][i] == self.table[0][i]
                  and self.table[1][i] == ' '):
                self.table[1][i] = char
                print(f'Making move level "{name}"')
                self.print_table()
                return True
        if (self.table[0][0] == char or self.table[0][0] == un_char) and self.table[0][0] == self.table[1][1] and \
                self.table[2][2] == ' ':
            self.table[2][2] = char
            print(f'Making move level "{name}"')
            self.print_table()
            return True
        if (self.table[0][2] == char or self.table[0][2] == un_char) and self.table[0][2] == self.table[1][1] and \
                self.table[2][0] == ' ':
            self.table[2][0] = char
            print(f'Making move level "{name}"')
            self.print_table()
            return True

    # дерево из тэйбла
    # стек
    def _max(self, char):
        max_value = -2
        line, col = None, None
        res = self.game_over()
        if char == 'X':
            if res == 'O wins':
                return -1, 0, 0
            elif res == 'X wins':
                return 1, 0, 0
            elif res == 'Draw':
                return 0, 0, 0
        elif char == 'O':
            if res == 'X wins':
                return -1, 0, 0
            elif res == 'O wins':
                return 1, 0, 0
            elif res == 'Draw':
                return 0, 0, 0
        for i in range(0, 3):
            for j in range(0, 3):
                if self.table[i][j] == ' ':
                    self.table[i][j] = char
                    m, min_i, min_j = self._min(char)
                    if m > max_value:
                        max_value = m
                        line = min_i
                        col = min_j
                    self.table[i][j] = ' '
        return max_value, line, col

    def _min(self, char):
        min_value = 2
        line, col = None, None
        res = self.game_over()
        if char == 'X':
            if res == 'O wins':
                return -1, 0, 0
            elif res == 'X wins':
                return 1, 0, 0
            elif res == 'Draw':
                return 0, 0, 0
        elif char == 'O':
            if res == 'X wins':
                return -1, 0, 0
            elif res == 'O wins':
                return 1, 0, 0
            elif res == 'Draw':
                return 0, 0, 0
        for i in range(0, 3):
            for j in range(0, 3):
                if self.table[i][j] == ' ':
                    self.table[i][j] = 'X' if char == 'O' else 'O'
                    m, max_i, max_j = self._max(char)
                    if m >= min_value:
                        min_value = m
                        line = max_i
                        col = max_j
                self.table[i][j] = ' '
        return min_value, line, col


# функция для вызова

command = input('Input command: ')
while not command == 'exit':
    if command.split(' ')[0] == 'start':
        if len(command.split(' ')) != 3:
            print('Bad parameters!')
            command = input('Input command: ')
        elif not (command.split(' ')[1] == 'user'
                  or command.split(' ')[1] == 'easy'
                  or command.split(' ')[1] == 'medium'
                  or command.split(' ')[1] == 'hard'):
            print('Bad parameters!')
            command = input('Input command: ')
        elif not (command.split(' ')[2] == 'user'
                  or command.split(' ')[2] == 'easy'
                  or command.split(' ')[2] == 'medium'
                  or command.split(' ')[2] == 'hard'):
            print('Bad parameters!')
            command = input('Input command: ')
        else:
            table_game = Table()
            table_game.print_table()
            if command.split()[1] == 'user':
                if command.split()[2] == 'easy':
                    result = False
                    while result is False:
                        table_game.valid_coordinates('X')
                        if not table_game.game_over():
                            table_game.randomize_coordinates('O', 'easy')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                elif command.split()[2] == 'user':
                    result = False
                    while result is False:
                        table_game.valid_coordinates('X')
                        if not table_game.game_over():
                            table_game.valid_coordinates('O')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                elif command.split()[2] == 'medium':
                    result = False
                    while result is False:
                        table_game.valid_coordinates('X')
                        if not table_game.game_over():
                            if not table_game.winner_or_scam_coordinates('O', 'medium'):
                                table_game.randomize_coordinates('O', 'medium')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                else:
                    result = False
                    while result is False:
                        table_game.valid_coordinates('X')
                        if not table_game.game_over():
                            pass
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
            elif command.split()[1] == 'easy':
                if command.split()[2] == 'easy':
                    result = False
                    while result is False:
                        table_game.randomize_coordinates('X', 'easy')
                        if not table_game.game_over():
                            table_game.randomize_coordinates('O', 'easy')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                elif command.split()[2] == 'user':
                    result = False
                    while result is False:
                        table_game.randomize_coordinates('X', 'easy')
                        if not table_game.game_over():
                            table_game.valid_coordinates('O')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                elif command.split()[2] == 'medium':
                    result = False
                    while result is False:
                        table_game.randomize_coordinates('X', 'easy')
                        if not table_game.game_over():
                            if not table_game.winner_or_scam_coordinates('O', 'medium'):
                                table_game.randomize_coordinates('O', 'medium')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                else:
                    result = False
                    while result is False:
                        table_game.randomize_coordinates('X', 'easy')
                        if not table_game.game_over():
                            pass
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
            elif command.split()[1] == 'medium':
                if command.split()[2] == 'easy':
                    result = False
                    while result is False:
                        if not table_game.winner_or_scam_coordinates('X', 'medium'):
                            table_game.randomize_coordinates('X', 'medium')
                        if not table_game.game_over():
                            table_game.randomize_coordinates('O', 'easy')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                elif command.split()[2] == 'medium':
                    result = False
                    while result is False:
                        if not table_game.winner_or_scam_coordinates('X', 'medium'):
                            table_game.randomize_coordinates('X', 'medium')
                        if not table_game.game_over():
                            if not table_game.winner_or_scam_coordinates('O', 'medium'):
                                table_game.randomize_coordinates('O', 'medium')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                elif command.split()[2] == 'user':
                    result = False
                    while result is False:
                        if not table_game.winner_or_scam_coordinates('X', 'medium'):
                            table_game.randomize_coordinates('X', 'medium')
                        if not table_game.game_over():
                            table_game.valid_coordinates('O')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                else:
                    result = False
                    while result is False:
                        if not table_game.winner_or_scam_coordinates('X', 'medium'):
                            table_game.randomize_coordinates('X', 'medium')
                        if not table_game.game_over():
                            pass
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
            else:
                if command.split()[2] == 'easy':
                    result = False
                    while result is False:
                        pass
                        if not table_game.game_over():
                            table_game.randomize_coordinates('O', 'easy')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                elif command.split()[2] == 'medium':
                    result = False
                    while result is False:
                        pass
                        if not table_game.game_over():
                            if not table_game.winner_or_scam_coordinates('X', 'medium'):
                                table_game.randomize_coordinates('X', 'medium')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                elif command.split()[2] == 'user':
                    result = False
                    while result is False:
                        pass
                        if not table_game.game_over():
                            table_game.randomize_coordinates('O', 'easy')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                else:
                    result = False
                    while result is False:
                        pass
                        if not table_game.game_over():
                            pass
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
