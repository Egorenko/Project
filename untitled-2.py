import time


class Table(list):  # игровое поле изначально пустое
    def __init__(self, score: int = None, initial_view: str = None, parent=None, children: list = None):
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

    def child(self, child):
        self.children.append(child)

    def __str__(self) -> str:
        value = '---------\n'
        for i in range(3):
            value += '| ' + ' '.join(c for c in self.table[i]) + ' |\n'
        value += '---------'
        return value

    def __repr__(self) -> str:
        return str(self.table)

    def game_over(self) -> str:  # проверка на конец игры
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

    def what_move(self):
        x_score = 0
        o_score = 0
        for i in range(3):
            for j in range(3):
                if self.table[i][j] == 'X':
                    x_score += 1
                elif self.table[i][j] == 'O':
                    o_score += 1
        if x_score <= o_score:
            return 'X'
        else:
            return 'O'

    @staticmethod
    def tree(parent=None):
        if parent is None:
            parent = Table()
        char = parent.what_move()
        for i in range(3):
            for j in range(3):
                if parent.table[i][j] == ' ':
                    parent.table[i][j] = char
                    parent.child(Table(initial_view=repr(parent), parent=parent))
                    parent.table[i][j] = ' '
        for child in parent.children:
            child.tree(parent=child)
        return parent

    def children_score(self, root=None):
        if root is None:
            tree = self.tree()  # создаем дерево
        else:
            tree = root
        for child in tree.children:  # переберимаем потомков
            res = child.game_over()  # проверяем на конец игры
            if res == 'X':
                child.children.clear()  # удаляем потомков, так как они не нужны
                child.score = 1
                break
            elif res == 'O':
                child.children.clear()
                child.score = -1
                break
            elif res == 'Draw':
                child.children.clear()
                child.score = 0
                break
            else:
                child.children_score(root=child)  # вызываем оценку потомков для этого потомка
        return tree

    def minimax(self, ai_char, root=None):
        tree = self.children_score(root)
        while tree.score is None:
            if all(map(lambda child: child.score is not None, tree.children)):
                if ai_char == tree.what_move():
                    tree.score = min(child.score for child in tree.children)
                else:
                    tree.score = max(child.score for child in tree.children)
            else:
                for child in tree.children:
                    child.minimax(ai_char, root=child)
        return tree.score

start_time = time.time()
table = Table()
table.minimax('X')
end_time = time.time()
print(f'{end_time - start_time} second')
