from vector import Vector

class Matrix:
    def __init__(self, rows: int, cols: int, data: list):
        if len(data) != rows:
            raise ValueError('The number of rows is invalid')
        
        for row in data:
            if len(row) != cols:
                raise ValueError('The number of columns is invalid')
            
        self.data = data
        self.rows = rows
        self.cols = cols
        
        
    def times(self, vector: Vector) -> Vector:
        if self.cols != len(vector):
            raise ValueError('Invalid operation for matrix and vector of these sizes')
        output = [0 for _ in range(len(vector))] 
        
        for i in range(0, len(self.rows)):
            for x in range(0, len(self.cols)):
                output[i] += self.data[i][x] * vector[x]
        
        return Vector(output) 
    

    def transpose(self) -> 'Matrix':
        newCols = self.rows
        newRows = self.cols 
        
        output = [[0 for _ in range(newCols)] for _ in range(newRows)]
        for col in range(0, self.cols):
            for row in range(0, self.rows):
                output[col][row] = self.data[row][col]
        
        return Matrix(newRows, newCols, output)
    

    def __str__(self) -> str:
        return f'Matrix: {"\n".join(self.data)}'
    
#https://towardsdatascience.com/math-neural-network-from-scratch-in-python-d6da9f29ce65

if __name__ == '__main__':
    v1 = Vector([1, 2, 3])
    m1 = Matrix(3, 3, [[3, 4, 5], [4, 5, 6], [7, 8, 9]])
    
    
        
        
                
                