class Vector:
    def __init__(self, data: list):
        self.data = data
        self.dimension = len(self.data)

    def __add__(self, other: 'Vector') -> 'Vector':
        if type(other) == Vector:
            return Vector([e1 + e2 for e1, e2 in zip(self.data, other.data)])
        else:
            return -1

    def __sub__(self, other: 'Vector') -> 'Vector':
        if type(other) == Vector:
            return Vector([e1 - e2 for e1, e2 in zip(self.data, other.data)])
        else:
            return -1

    def dot(self, other: 'Vector') -> 'Vector':
        if type(other) == Vector:
            return sum([e1 * e2 for e1, e2 in zip(self.data, other.data)])
        else:
            return -1
        
    def __str__(self) -> str:
        return f'Vector: ({self.data})'


if __name__ == '__main__':
    v1 = Vector([1, 2, 3])
    v2 = Vector([5, 5, 7])

    print(v1 + v2)
    print(v1 - v2)
    print(v1.dot(v2))
