from random import random


class Matrix:
    def __init__(self, rows: int, cols: int, data: list = None):
        if data == None:
            self.data = [[0 for _ in range(cols)]
                         for _ in range(rows)]
        else:
            if len(data) != rows:
                raise ValueError('The number of rows is invalid')

            for row in data:
                if len(row) != cols:
                    raise ValueError('The number of columns is invalid')
                
            self.data = data
        self.rows = rows
        self.cols = cols

    def randomInit(self):
        for i in range(0, self.rows):
            for x in range(0, self.cols):
                self.data[i][x] = random()

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if other.cols == self.cols and other.rows == self.rows:
            output = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            for i in range(0, self.rows):
                for x in range(0, self.cols):
                    output[i][x] = self.data[i][x] + other.data[i][x]

            return Matrix(self.rows, self.cols, output)

        else:
            raise ValueError('Invalid matrix dimensions')

    def __sub__(self, other: 'Matrix'):
        if other.cols == self.cols and other.rows == self.rows:
            output = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            for i in range(0, self.rows):
                for x in range(0, self.cols):
                    output[i][x] = self.data[i][x] - other.data[i][x]

            return Matrix(self.rows, self.cols, output)

        else:
            raise ValueError('Invalid matrix dimensions')

    def __mul__(self, other):
        if type(other) == float:
            output = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            for i in range(0, self.rows):
                for x in range(0, self.cols):
                    output[i][x] = self.data[i][x] * other

            return Matrix(self.rows, self.cols, output)

        elif type(other) == Matrix:
            if self.cols == other.rows:
                output = [[0 for _ in range(other.cols)]
                          for _ in range(self.rows)]

                for i in range(0, self.rows):
                    row = self.data[i]

                    for x in range(0, other.cols):
                        total = 0
                        for z in range(0, other.rows):
                            total += row[z] * other.data[z][x]
                        output[i][x] = total

                return Matrix(self.rows, other.cols, output)
            else:
                raise ValueError('Inavlid matrix dimensions')
        else:
            raise ValueError('Invalid operand type')

    def transpose(self) -> 'Matrix':
        newCols = self.rows
        newRows = self.cols

        output = [[0 for _ in range(newCols)] for _ in range(newRows)]
        for col in range(0, self.cols):
            for row in range(0, self.rows):
                output[col][row] = self.data[row][col]

        return Matrix(newRows, newCols, output)

    def __str__(self) -> str:
        output = 'Matrix: \n'
        for row in self.data:
            output += str(row) + '\n'
        return output



if __name__ == '__main__':
    m1 = Matrix(2, 2, [[1, 2], [3, 4]])
    m2 = Matrix(2, 1, [[4], [5]])
    print(m1 * m2)
