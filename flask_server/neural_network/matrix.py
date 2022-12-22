from random import random


class Matrix:
    def __init__(self, rows: int, cols: int, data: list = None):
        if data == None:
            # if no data is given initialize array full of zeros
            self.data = [[0 for _ in range(cols)]
                         for _ in range(rows)]
        else:
            # look for descrepancies in the shape of the data and the values passed for the rows and columns
            if len(data) != rows:
                raise ValueError('The number of rows is invalid')

            for row in data:
                if len(row) != cols:
                    raise ValueError('The number of columns is invalid')

            self.data = data
        self.rows = rows
        self.cols = cols

    def randomInit(self):
        # add random values to the array used to represent the matrix
        for i in range(0, self.rows):
            for x in range(0, self.cols):
                self.data[i][x] = random()

    def __add__(self, other: 'Matrix') -> 'Matrix':
        # override standard addition operator to add matrix to another matrix
        #this function simply performs component-wise addition
        
        if other.cols == self.cols and other.rows == self.rows:
            output = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            for i in range(0, self.rows):
                for x in range(0, self.cols):
                    output[i][x] = self.data[i][x] + other.data[i][x]

            return Matrix(self.rows, self.cols, output)

        else:
            raise ValueError('Invalid matrix dimensions')

    def __sub__(self, other: 'Matrix'):
        # override standard addition operator to subtract matrix from another matrix
        #this function simply performs component-wise subtraction
        if other.cols == self.cols and other.rows == self.rows:
            output = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            for i in range(0, self.rows):
                for x in range(0, self.cols):
                    output[i][x] = self.data[i][x] - other.data[i][x]

            return Matrix(self.rows, self.cols, output)

        else:
            raise ValueError('Invalid matrix dimensions')

    def __mul__(self, other):
        # function used to perform matrix-matrix multiplication and matrix-scalar multiplication
        #both forms of multiplication use the standard mathematical definitions
        
        # matrix-scalar multiplication
        if type(other) == float:
            output = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            for i in range(0, self.rows):
                for x in range(0, self.cols):
                    output[i][x] = self.data[i][x] * other

            return Matrix(self.rows, self.cols, output)

        # matrix-matrix multiplication
        elif 'Matrix' in str(type(other)):
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

    def hadamardProduct(self, other: 'Matrix') -> 'Matrix':
        # Function to compute the hadamard product of two matrices, also known as component-wise multiplication
        output = self.data

        if other.rows != self.rows or other.cols != self.cols:
            raise ValueError('The two matrices must have the same diemnsions')

        for i in range(0, self.rows):
            for x in range(0, self.cols):
                output[i][x] *= other.data[i][x]

        return Matrix(self.rows, self.cols, output)

    def transpose(self) -> 'Matrix':
        # Function used to transpose a matrix
        #columns are convered into rows, but the order is perserved
        newCols = self.rows
        newRows = self.cols

        output = [[0 for _ in range(newCols)] for _ in range(newRows)]
        for col in range(0, self.cols):
            for row in range(0, self.rows):
                output[col][row] = self.data[row][col]

        return Matrix(newRows, newCols, output)

    def __str__(self) -> str:
        # Override str() method to show a more informative represetation of the matrix
        output = 'Matrix: \n'
        for row in self.data:
            output += str(row) + '\n'
        return output


if __name__ == '__main__':
    m1 = Matrix(2, 2, [[1, 2], [3, 4]])
    m2 = Matrix(2, 1, [[4], [5]])
    m3 = Matrix(3, 3)
    m3.randomInit()
    m4 = Matrix(2, 2, [[3, 4], [5, 6]])
    
    print(m3) #test randomInit and __str__ methods
    print(m1 + m4) #test __add__ methods, expect[[4, 6], [8, 10]]
    print(m1 * m2) #test __mul__ method, expect [[14, 32]]
    print(m1 * 5.0) #test __mul__ method, expect [[5, 10], [15, 20]]
    print(m1.hadamardProduct(m4)) #test hadamardProduct method expect [[3, 8], [15, 24]]
    print(m1 - m4) #test __sub__ method expect [[0, 4], [10, 18]]
