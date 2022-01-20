import time


class Table(list):  # игровое поле изначально пустое
    def __init__(self, score: int = None,
                 initial_view: str = None,
                 parent=None,
                 children: list = None,
                 moves: str = None):
        super().__init__()
        if initial_view:  # строка вида [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            self.table = [[initial_view[i] for i in range(3, 14, 5)],
                          [initial_view[i] for i in range(20, 31, 5)],
                          [initial_view[i] for i in range(37, 48, 5)]]
        else:
            self.table = [[' ' for _ in range(3)] for _ in range(3)]
        self.parent = parent
        self.children = []
        if children:
            self.children = children
        self.score = score
        self.is_over = False
        if (''.join(c for c in map(''.join, self.table)).count('X') <=
                ''.join(c for c in map(''.join, self.table)).count('O')):
            self.char = 'X'
        else:
            self.char = 'O'
        self.result = False
        self.moves = ''
        if moves:
            self.moves = moves

    def child(self, child):
        self.children.append(child)

    def plus_move(self, move: str):
        self.moves += move

    def minus_move(self):
        self.moves = self.moves[0:-2]

    def __str__(self) -> str:
        value = '---------\n'
        for i in range(3):
            value += '| ' + ' '.join(c for c in self.table[i]) + ' |\n'
        value += '---------'
        return value

    def __repr__(self) -> str:
        return str(self.table)

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
        return False

    @staticmethod
    def tree(root=None, ai_char='X'):
        if root is None:
            parent = Table()
        else:
            parent = root
        for i in range(3):
            for j in range(3):
                if parent.table[i][j] == ' ':
                    parent.table[i][j] = parent.char
                    parent.plus_move(f'{i}{j}')
                    parent.child(Table(initial_view=repr(parent), parent=parent, moves=parent.moves))
                    parent.minus_move()
                    parent.table[i][j] = ' '
        for child in parent.children:
            if not child.game_over():
                child.tree(root=child)
            else:
                child.is_over = True
                child.result = child.game_over()
                if child.result == 'Draw':
                    child.score = 0
                else:
                    if child.result != ai_char:
                        child.score = -1
                    else:
                        child.score = 1
        return parent

    def children_score(self, ai_char='X', root=None, is_one=True):
        if is_one:
            tree = self.tree(root=root)
            is_one = False
        else:
            tree = root
        if tree.score is None:
            for child in tree.children:  # переберимаем потомков
                if child.score is not None:
                    continue
                else:
                    res = child.game_over()  # проверяем на конец игры
                    if res == 'Draw':
                        child.score = 0
                    elif res == ai_char:
                        child.score = 1
                    else:
                        if res is not False:
                            child.score = -1
                        else:
                            child.children_score(root=child, is_one=is_one)  # вызываем оценку потомков для этого
                            # потомка
        if all(map(lambda baby: baby.score is not None, tree.children)):
            if ai_char == tree.char:
                tree.score = max(child.score for child in tree.children)
            else:
                tree.score = min(child.score for child in tree.children)
        return self

    def minimax(self, ai_char='X', root=None):
        tree = self.children_score(root=root)
        for child in tree.children:
            if child.score == tree.score:
                line = int(child.moves[-2])
                col = int(child.moves[-1])
                self.table[line][col] = ai_char
                print(self)
                break
        return self.table

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
                    print(self)
                    return True
        self.valid_coordinates(char)


table = Table(initial_view="[['X', ' ', ' '], ['X', ' ', 'O'], ['O', ' ', ' ']]")
start = time.time()
while not table.game_over():
    table.minimax(root=table)
    if not table.game_over():
        table.valid_coordinates('O')
end = time.time()
print(f'{end - start} sec')
