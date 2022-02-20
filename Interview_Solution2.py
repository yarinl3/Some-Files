__author__ = 'Yarin Levi'
__email__ = 'yarinl330@gmail.com'
"""
My solution for 'Medium Google Coding Interview With Ben Awad'
https://www.youtube.com/watch?v=4tYoVx0QoN0
"""

white_list = set()


def main():
    global white_list

    matrix = [[1, 0, 0, 0, 0, 0],
              [0, 1, 0, 1, 1, 1],
              [0, 0, 1, 0, 1, 0],
              [1, 1, 0, 0, 1, 0],
              [1, 0, 1, 1, 0, 0],
              [1, 0, 0, 0, 0, 1]]
    [white_list.add((0, i)) for i in range(len(matrix[0])) if matrix[0][i] == 1]
    [white_list.add((len(matrix) - 1, i)) for i in range(len(matrix[-1])) if matrix[-1][i] == 1]
    [white_list.add((i, 0)) for i in range(len(matrix)) if matrix[i][0] == 1]
    [white_list.add((i, len(matrix[i]) - 1)) for i in range(len(matrix)) if matrix[i][-1] == 1]
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):
            foo(matrix, i, j)
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):
            if matrix[i][j] == 1 and (i, j) not in white_list:
                matrix[i][j] = 0
    print(matrix)


def foo(matrix, i, j):
    global white_list

    if matrix[i][j] == 0 or matrix[i][j] in white_list:
        return
    top = (i+1, j)
    bottom = (i-1, j)
    right = (i, j+1)
    left = (i, j-1)
    if True in [True for index in [top, bottom, right, left] if index in white_list]:
        white_list.add((i, j))
        if matrix[i+1][j] == 1 and top not in white_list:
            foo(matrix, i+1, j)
        if matrix[i-1][j] == 1 and bottom not in white_list:
            foo(matrix, i-1, j)
        if matrix[i][j+1] == 1 and right not in white_list:
            foo(matrix, i, j+1)
        if matrix[i][j-1] == 1 and left not in white_list:
            foo(matrix, i, j-1)


if __name__ == '__main__':
    main()
