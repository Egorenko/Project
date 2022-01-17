from anytree import RenderTree, AsciiStyle, Node


class Table(list):  # игровое поле изначально пустое
    def __init__(self, initial_view: str = None, parent=None, children=None):
        super().__init__()
        if initial_view:  # строка вида [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            self.table = [[initial_view[i] for i in range(3, 14, 5)],
                          [initial_view[i] for i in range(20, 31, 5)],
                          [initial_view[i] for i in range(37, 48, 5)]]
        else:
            self.table = [[' ' for _ in range(3)] for _ in range(3)]
        self.parent = parent
        if children:
            self.children = children

    def __str__(self):
        value = '---------\n'
        for i in range(3):
            value += '| ' + ' '.join(c for c in self.table[i]) + ' |\n'
        value += '---------'
        return value

    def __repr__(self):
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

    def minimax(self, char, parent=None):  # без рекурсии, только 9 первых потомков
        max_score = -2  # значение очков условно для крестиков, потом это будет для ИИ
        min_score = 2  # значение условно для ноликов, а это будет для противника
        score = max_score  # первые крестики, поэтому выбираем их значение очков
        move_x, move_y = None, None
        res = self.game_over()  # проверяем на конец игры
        if res == 'X':
            return 1, 'w', 'w'
        elif res == 'O':
            return -1, 'l', 'l'
        elif res == 'Draw':
            return 0, 'd', 'd'
        if parent is None:
            root = Table()
            parent = root
        for i in range(3):
            for j in range(3):
                if parent.table[i][j] == ' ':
                    parent.table[i][j] = char
                    child = Table(initial_view=repr(parent), parent=parent)
                    parent.table[i][j] = ' '
        for child in parent.children:
            print(child)
        return score, move_x, move_y


table = Table()
table.minimax('X')
