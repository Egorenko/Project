import random
from anytree import RenderTree, AsciiStyle, Node, NodeMixin


class Table(list):  # игровое поле изначально пустое
    def __init__(self):
        super().__init__()
        self.table = [[' ' for _ in range(3)] for _ in range(3)]

    def print_table(self):
        print('---------')
        for i in range(3):
            print('|', *self.table[i], '|', sep=' ')
        print('---------')

    def return_table(self):
        return str(self.table)  # чтобы в узлах дерева была не ссылка на одну доску, а ее состояние с тем ходом

    def game_over(self):  # проверка на конец игры
        for i in range(3):  # победа по горизонтали
            if self.table[i][0] != ' ' and self.table[i] == [self.table[i][0] for _ in range(3)]:
                return self.table[i][0]
        for i in range(3):  # победа по вертикали
            if (self.table[0][i] != ' '
                    and self.table[0][i] == self.table[1][i]
                    and self.table[1][i] == self.table[2][i]):
                return self.table[0][i]
        if self.table[0][0] != ' ' and all(self.table[0][0] == self.table[i][i] for i in range(1, 3)):
            return self.table[0][0]  # победа по главной диагонали
        if self.table[0][2] != ' ' and all(self.table[0][2] == self.table[i][2 - i] for i in range(1, 3)):
            return self.table[0][2]  # победа по побочной диагонали
        not_empty = True
        for line in self.table:
            if ' ' in line:
                not_empty = False
        if not_empty:
            return 'Draw'  # ничья

    def valid_coordinates(self, char):
        coordinates = input('Enter the coordinates: ')
        if not (coordinates[0].isdigit() and coordinates[2].isdigit()):
            print('You should enter numbers!')
        else:
            if not (1 <= int(coordinates[0]) <= 3 and 1 <= int(coordinates[2]) <= 3):
                print('Coordinates should be from 1 to 3!')
            else:
                if not (self.table[int(coordinates[0]) - 1][int(coordinates[2]) - 1] == ' '):
                    print('This cell is occupied! Choose another one!')
                else:
                    self.table[int(coordinates[0]) - 1][int(coordinates[2]) - 1] = char
                    self.print_table()
                    return True
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

    def winner_or_scum_coordinates(self, char, name):
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
            if ((self.table[0][i] == char or self.table[0][i] == un_char)
                    and self.table[1][i] == self.table[0][i]
                    and self.table[2][i] == ' '):
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
        if ((self.table[0][0] == char or self.table[0][0] == un_char)
                and self.table[0][0] == self.table[1][1]
                and self.table[2][2] == ' '):
            self.table[2][2] = char
            print(f'Making move level "{name}"')
            self.print_table()
            return True
        if ((self.table[0][2] == char or self.table[0][2] == un_char)
                and self.table[0][2] == self.table[1][1]
                and self.table[2][0] == ' '):
            self.table[2][0] = char
            print(f'Making move level "{name}"')
            self.print_table()
            return True

    def minimax(self, char, parent=None):  # без рекурсии, только 9 первых потомков
        max_score = -2  # значение очков условно для крестиков, потом это будет для ИИ
        min_score = 2  # значение условно для ноликов, а это будет для противника
        score = max_score  # первые крестики, поэтому выбираем их значение очков
        res = self.game_over()  # проверяем на конец игры
        if res == 'X':
            return 1
        elif res == 'O':
            return -1
        elif res == 'Draw':
            return 0
        start = Node(self.return_table(), parent)  # создаем корневой узел в виде пустого поля
        parent = start  # делаем его родиетелем для следующих узлов
        for i in range(3):
            for j in range(3):
                if self.table[i][j] == ' ':
                    self.table[i][j] = char  # делаем ход
                    a = Node(self.return_table(), parent=parent)  # создаем узлы с этим ходом
                    self.table[i][j] = ' '  # убираем ход
        with open('output.txt', 'a', encoding='utf-8') as fil:
            print(RenderTree(start, style=AsciiStyle()).by_attr(), score, file=fil)
            print(start.children, file=fil)  # это вывод в файл, потому что читать в консоли было неудобно
        return score  # возвращаем очки для доски


# так по факту должен выглядеть класс доски, чтобы его можно было просто
# наследовать как узлы дерева
# тогда минимакс нужно определять в нем и давать ИИ работать с отдельной доской для построения дерева
class TableTree(Table, NodeMixin):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def minimax(self, char, parent=None):
        pass


# функция для вызова - ее еще нет
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
            # table_game.mini()
            table_game.minimax('X')
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
                        if not table_game.game_over():
                            table_game.valid_coordinates('X')
                            if not table_game.game_over():
                                table_game.valid_coordinates('O')
                            else:
                                result = table_game.game_over()
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
                            if not table_game.winner_or_scum_coordinates('O', 'medium'):
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
                            if not table_game.winner_or_scum_coordinates('O', 'medium'):
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
                        if not table_game.winner_or_scum_coordinates('X', 'medium'):
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
                        if not table_game.winner_or_scum_coordinates('X', 'medium'):
                            table_game.randomize_coordinates('X', 'medium')
                        if not table_game.game_over():
                            if not table_game.winner_or_scum_coordinates('O', 'medium'):
                                table_game.randomize_coordinates('O', 'medium')
                        else:
                            result = table_game.game_over()
                    else:
                        print(result)
                        command = input('Input command: ')
                elif command.split()[2] == 'user':
                    result = False
                    while result is False:
                        if not table_game.winner_or_scum_coordinates('X', 'medium'):
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
                        if not table_game.winner_or_scum_coordinates('X', 'medium'):
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
                            if not table_game.winner_or_scum_coordinates('X', 'medium'):
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
