def matrix(s):
    s = s.split()
    matrix = [['0' for _ in range(int(s[1]))] for _ in range(int(s[0]))]
    count = [int(i) for i in range(1, int(s[0]) * int(s[1]) + 1)]
    napr = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    nomernapr = 0
    i = 0
    j = 0
    while len(count) != 0:
        print(matrix)
        print(nomernapr)
        if i <= int(s[1]) - 1 and j <= int(s[0]):
            if matrix[i][j] == '0':
                matrix[i][j] = str(count[0])
                del count[0]
            else:
                nomernapr += 1
                i += napr[nomernapr][1]
                j += napr[nomernapr][0]
            if i < len(matrix) and j < len(matrix[i]) - 1:
                i += napr[nomernapr][1]
                j += napr[nomernapr][0]
            else:
                nomernapr += 1
                i += napr[nomernapr][1]
                j += napr[nomernapr][0]
    return matrix

print(*(' '.join(c) for c in matrix(input())), sep='\n')